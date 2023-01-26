from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine.defaults import DefaultPredictor
import cv2
import settings
import os


cfg = get_cfg()
cfg.merge_from_file(
    model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")
)
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"
)
try:
    # It may fail if no GPU was found
    DET_MODEL = DefaultPredictor(cfg)
except:
    # Load the model for CPU only
    print(
        f"Failed to load Detection model on GPU, "
        "trying with CPU. Message: {exp}."
    )
    cfg.MODEL.DEVICE='cpu'
    DET_MODEL = DefaultPredictor(cfg)


def get_vehicle_coordinates(img):
    print(img)
    # img = cv2.imread(os.path.join(settings.UPLOAD_FOLDER,img))
    # print(img)
    outputs = DET_MODEL(img)
    interest_classes = [2,7]
    classes = outputs["instances"].pred_classes.cpu().numpy()
    boxes = outputs["instances"].pred_boxes.tensor.cpu().numpy()
    print(img)
    print(boxes)
    box_coordinates=[]
    if boxes is not None:
        print('primer if')
        n = classes.shape[0]
        interest_bboxes = []
        for i in range(n):
            if classes[i] in interest_classes:
                interest_bboxes.append(boxes[i,:].astype(int))
        area=0
        if interest_bboxes is not None:
            for box in interest_bboxes:
                area1=(box[2]-box[0])*(box[3]-box[1])
                print(area1)
                if area1>area:
                    area = area1
                    box_coordinates=[box[0],box[1],box[2],box[3]]
        else:
            box_coordinates = [0,0,0,0]
    else:
        box_coordinates = [0,0,0,0]
    if len(box_coordinates)==0:
        box_coordinates = [0,0,0,0]
    return box_coordinates
