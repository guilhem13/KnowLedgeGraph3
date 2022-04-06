import ast
import multiprocessing as mp
import requests
import arxiv

from bdd.paper_model_orm import PapierORM
from knowledgegraph.controller.data.arxiv import Data
from knowledgegraph.controller.treatment.mainprocess import Pipeline
from knowledgegraph.models import Entity, Papier
from knowledgegraph.owl import ontology
from main import services_manager , remove_file

"""
route --- getner part 
"""

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


"""
route --- feedbdd part 
"""


def feed_bdd(nb_paper, session):

    client_arxiv = arxiv.Client(page_size=nb_paper, delay_seconds=3, num_retries=5)
    converter = Data(nb_paper)
    for result in client_arxiv.results(
        arxiv.Search(
            query="cat:cs.AI",
            max_results=nb_paper,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )
    ):
        list_of_entites = converter.process_authors(result.authors)
        list_of_entites = [x.__dict__ for x in list_of_entites]
        p = PapierORM(
            converter.get_doi(result.entry_id),
            result.title,
            str(list_of_entites),
            result.pdf_url,
            result.summary,
            str(result.published),
        )
        if session.query(PapierORM).first() == None:
            session.add(p)
            session.commit()
        else:
            if session.query(PapierORM).filter(PapierORM.doi == p.doi).scalar() is None:
                session.add(p)
                session.commit()


"""
route --- pipeline
"""
def arxiv_route_main_function(block_paper):

    p = Pipeline("https://export.arxiv.org/pdf/", 0)
    out_queue = mp.Queue()
    batch_size = 5
    return p.make_traitement_pipeline(block_paper, out_queue, batch_size)

def pipeline_from_arxiv(nb_paper):
    nb_paper_to_request = int(nb_paper)
    block_arxiv_size = 5
    arxiv_data = Data(nb_paper_to_request).get_set_data()
    papiers = []
    
    quotient = nb_paper_to_request / block_arxiv_size
    owl = ontology.Ontology()

    if quotient > 1:
        length = int(block_arxiv_size * quotient)
        stop = 0
        for i in range(0, length, block_arxiv_size):
            print(i)
            if i + block_arxiv_size < length + 1:
                stop += 5
                temp_papiers = arxiv_route_main_function(arxiv_data[i : i + block_arxiv_size])
                if len(temp_papiers)>0:
                    for papier in temp_papiers:
                        papier.datepublished = str(papier.datepublished)
                        if len(papier.entities_from_reference) < 15:
                            response = requests.post(papier.link+".pdf")
                            with open("knowledgegraph/file/"+papier.doi+".pdf", 'wb') as f:
                                f.write(response.content)
                            papier = services_manager(papier)
                            remove_file(papier)

                    for papier in temp_papiers: 
                        owl.add_papier(papier)
                    owl.save('knowledgegraph/owl/onto10.owl')

        if nb_paper_to_request - stop > 0:
            temp_papiers = arxiv_route_main_function(arxiv_data[stop:nb_paper_to_request])
            if len(temp_papiers)>0:
                for papier in temp_papiers:
                    papier.datepublished = str(papier.datepublished)
                    if len(papier.entities_from_reference) < 15:
                        response = requests.post(papier.link+".pdf")
                        with open("knowledgegraph/file/"+papier.doi+".pdf", 'wb') as f:
                            f.write(response.content)
                        papier = services_manager(papier)
                        remove_file(papier)

                for papier in temp_papiers: 
                    owl.add_papier(papier)
                owl.save('knowledgegraph/owl/onto10.owl')
    else:
        temp_papiers = arxiv_route_main_function(arxiv_data[0:nb_paper_to_request])
        if len(temp_papiers)>0:
            for papier in temp_papiers:
                papier.datepublished = str(papier.datepublished) # ajout
                if len(papier.entities_from_reference) < 15:
                    response = requests.post(papier.link+".pdf")
                    with open("knowledgegraph/file/"+papier.doi+".pdf", 'wb') as f:
                        f.write(response.content)
                    papier = services_manager(papier)
                    remove_file(papier)

            for papier in temp_papiers: 
                owl.add_papier(papier)
            owl.save('knowledgegraph/owl/onto10.owl')
    print(len(papiers))
    

