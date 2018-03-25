import sys
import os

p3_version = (3,0)
cur_version = sys.version_info

if cur_version < p3_version:
    reload(sys)
    sys.setdefaultencoding('utf-8')

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib'))
sys.path.append(os.path.abspath(os.getcwd()))    
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from csv_data_uploader import CSVDataUploader
from database import init_db
from tasks import load_comments_from_se_to_db, analyse_comments, create_model, check_to_rebuild, play, dump_verified_comments

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

        if str(sys.argv[1]) == "--create-model":
            create_model() 
            sys.exit() 

        if str(sys.argv[1]) == "--check-to-rebuild":
            check_to_rebuild() 
            sys.exit()

        if str(sys.argv[1]) == "--play":
            play() 
            sys.exit()

        if str(sys.argv[1]) == "--dump-comments":
            dump_verified_comments() 
            sys.exit()            

        if str(sys.argv[1]) == "--load-dumped-comments":
            uploader = CSVDataUploader("dump/")
            uploader.from_dump() 
            sys.exit()                        

        print("Wrong parameters. Check the spelling.")
        sys.exit()

    app.run()