from talon.signature.learning.dataset import build_extraction_dataset
from talon.signature.learning import classifier as c

build_extraction_dataset("../forge/dataset/P", "./talon/signature/data/train.data")
c.train(c.init(), "./talon/signature/data/train.data", "./talon/signature/data/classifier")