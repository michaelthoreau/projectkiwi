import sys,os
sys.path.insert(0, os.getcwd())
from projectkiwi.connector import Connector
from projectkiwi.models import  Annotation
from projectkiwi.tools import getBboxTileCoords
import numpy as np

from test_basics import TEST_URL


def test_read_annotations():
    API_KEY = os.environ['PROJECT_KIWI_API_KEY']

    conn = Connector(API_KEY, TEST_URL)

    annotations = conn.getAnnotations()

    assert len(annotations) >= 1, "Missing Annotations"


def test_read_annotations():
    API_KEY = os.environ['PROJECT_KIWI_API_KEY']

    conn = Connector(API_KEY, TEST_URL)

    annotations = conn.getAnnotations()

    assert len(annotations) >= 1, "Missing Annotations"


def test_annotations_in_tile():
    API_KEY = os.environ['PROJECT_KIWI_API_KEY']

    conn = Connector(API_KEY, TEST_URL)

    project = conn.getProjects()[0]

    allAnnotations = conn.getAnnotations(project=project)

    annotations = conn.getAnnotationsForTile(
            annotations=allAnnotations,
            zxy = "12/1051/1522",
            overlap_threshold=0.2)

    assert len(annotations) > 0, "No annotations found for tile"


def test_get_bboxes_for_tile():
    API_KEY = os.environ['PROJECT_KIWI_API_KEY']

    conn = Connector(API_KEY, TEST_URL)

    project = conn.getProjects()[0]

    allAnnotations = conn.getAnnotations(project=project)

    tile_zxy = "12/1051/1522"
    annotations = conn.getAnnotationsForTile(
            annotations=allAnnotations,
            zxy = tile_zxy,
            overlap_threshold=0.2)

    assert len(annotations) > 0, "No annotations found for tile"

    for annotation in annotations:
        bbox = getBboxTileCoords(annotation.coordinates, tile_zxy)
        assert len(bbox) == 4, "malformed bounding box"


def test_read_predictions():
    API_KEY = os.environ['PROJECT_KIWI_API_KEY']

    conn = Connector(API_KEY, TEST_URL)

    predictions = conn.getPredictions()

    assert len(predictions) >= 1, "Missing predictions"


def test_dict_conversion():
    API_KEY = os.environ['PROJECT_KIWI_API_KEY']

    conn = Connector(API_KEY, TEST_URL)

    project = conn.getProjects()[0]

    annotation = conn.getAnnotations(project=project)[0]

    annoDict = dict(annotation)
    newAnnotation = Annotation.from_dict(annoDict)
    assert annotation == newAnnotation, "Bad dict convesion"




def test_add_annotation():
    API_KEY = os.environ['PROJECT_KIWI_API_KEY']

    conn = Connector(API_KEY, TEST_URL)

    project = conn.getProjects()[0]

    annotation = Annotation(
        shape="Polygon",
        label_id=374,
        imagery_id="93650ec6508a",
        coordinates=[
            [-87.612448, 41.867452], 
            [-87.605238, 41.867452], 
            [-87.605238, 41.852301], 
            [-87.612448, 41.852301], 
            [-87.612448, 41.867452]]
    )


    success = conn.addAnnotation(annotation, project)
    assert success, "Failed to add annotation"

def test_add_prediction():
    API_KEY = os.environ['PROJECT_KIWI_API_KEY']

    conn = Connector(API_KEY, TEST_URL)

    project = conn.getProjects()[0]

    prediction = Annotation(
        shape="Polygon",
        label_id=374,
        imagery_id="93650ec6508a",
        coordinates=[
            [-87.612448, 41.867452], 
            [-87.605238, 41.867452], 
            [-87.605238, 41.852301], 
            [-87.612448, 41.852301], 
            [-87.612448, 41.867452]],
        confidence = 0.33
    )


    success = conn.addPrediction(prediction, project)
    assert success, "Failed to add prediction"
