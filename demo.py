from housing.pipeline.pipeline import Pipleine
from housing.exception import HousingException
import os,sys


def main():
    try:
        pipeline=Pipleine()
        pipeline.run_pipeline()
    except Exception as e:
        raise HousingException(e,sys) from e


if __name__=="__main__":
    main()