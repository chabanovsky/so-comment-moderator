import sys
import os

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib'))
sys.path.append(os.path.abspath(os.getcwd()))    
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from csv_data_uploader import CSVDataUploader
from database import init_db
from tasks import load_comments_from_se_to_db, analyse_comments, create_model

from meta import *
from views import *
from filters import *

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if str(sys.argv[1]) == "--upload-data":
            uploader = CSVDataUploader()
            uploader.cvs_to_db()
            sys.exit()

        if str(sys.argv[1]) == "--init-db":
            init_db() 
            sys.exit()   
        
        if str(sys.argv[1]) == "--comments-from-se-to-db":
            load_comments_from_se_to_db() 
            sys.exit()   

        if str(sys.argv[1]) == "--analyse":
            analyse_comments() 
            sys.exit()   

        if str(sys.argv[1]) == "--create_model":
            create_model() 
            sys.exit() 

        print("Wrong parameters. Check the spelling.")
        sys.exit()

    app.run()