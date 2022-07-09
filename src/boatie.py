import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import gspread
import matplotlib
import ftplib
from ftplib import FTP
from datetime import datetime

SHEETSKEY = 'XXX'

# Link with Google Sheets
gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key(SHEETSKEY)
worksheet = sh.worksheet("Totals")

# Image file name
date = datetime.now().strftime("%Y-%m-%d-%H-%M")
short_date = datetime.now().strftime("%H")
file_name = "pcbc-" + date + ".png"
directory = "res/" + file_name
online_file_name = "pcbc-" + short_date + ".png"

def load_data():
    col2 = worksheet.col_values(2)
    col6 = worksheet.col_values(7)
    teams = col2[4:9]
    points_string = col6[4:9]
    points = []

    for point in points_string:
        points.append(int(point))
    return points, teams 

def plot_graph():

    # Inital
    points, teams = load_data()
    y_pos = np.arange(len(teams))  
    maxpoint = max(points)
    minpoint = min(points)
    fig, ax = plt.subplots()

    # Boat points
    paths = ['res/Argives.png','res/Myrmidons.png','res/Locrians.png','res/Epeans.png','res/Symians.png']
    paths.reverse()
    # Build scale
    sortedpoints = sorted(points)
    minpoint = min(points)
    scaledpoints = [x/minpoint for x in points]
    scales = [0]*5
    for i in range(0,5):
        point = points[i]
        place = sortedpoints.index(point) 
        scales[i] = 0.11+0.01*place

    x = points
    y = y_pos

    for x0, y0, path, scale in zip(y,x,paths,scales):
        ab = AnnotationBbox(OffsetImage(plt.imread(path),zoom=scale), (x0, y0), frameon=False)
        ax.add_artist(ab)

    plt.scatter(y,x,zorder=1)

    results = zip(y,x,paths,scales)

    # Remove borders
    ax=plt.gca() 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.ylabel('Points')
    plt.xlim(-1.5, y_pos[-1]+1.5)
    plt.ylim(minpoint-0.3*maxpoint,1.3*maxpoint)
    plt.xticks(y_pos,teams,rotation=90)
    plt.gca().invert_yaxis()

    # River background
    river = plt.imread("res/river.jpg")
    plt.imshow(river, zorder=0, extent=[-1.5,y_pos[-1]+2,1.3*maxpoint, minpoint-0.3*maxpoint], aspect='auto')

    # Save
    plt.savefig(directory,dpi=300, bbox_inches='tight')

def upload():
    session = ftplib.FTP(HOST,ADDRESS,KEY)
    session.cwd('public_html') 
    # file to send
    file = open(directory,'rb') 
    # send the file
    session.storbinary('STOR {}'.format(online_file_name), file)     
    # close file and FTP
    file.close()                                    
    session.quit()

def update():
    WEBSITE = 'URL'
    url = WEBSITE + online_file_name
    worksheet.update_cell(50,25,'=IMAGE("'+url+'",1)')

load_data()
plot_graph()
# upload()
# update()






