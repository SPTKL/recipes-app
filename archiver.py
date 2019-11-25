from cook import Archiver
import os 

archiver = Archiver(engine=os.environ['RECIPE_ENGINE'], 
                    ftp_prefix=os.environ['FTP_PREFIX'])