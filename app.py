
#rough
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import torchvision
from torchvision.models.detection import SSDLite320_MobileNet_V3_Large_Weights
import imutils
from yolo_code import detect_objects_in_frame
# from ssd_code import detect_objects_in_frame_ssd
#from pymongo import MongoClient 
import cv2
import cv2
import numpy as np

from ultralytics import YOLO
from supervision.detection.core import Detections
from tkinter import Label
#import ttkbootstrap

tk = Tk()
#tk=ttkbootstrap.Window()
tk.resizable(0,0)
tpic=[]
success=True
count=1
ncount=0
tcount=0
cap = cv2.VideoCapture(0)
#VIDEO CAPTURE IN LABLE
#cap = cv2.VideoCapture("rtsp://admin:admin@123@192.168.3.156")
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

model_roboflow_agumentation = YOLO('')
# model_manual_agumentation = YOLO('')



# def capture():
#     global video_capture
#     video_capture = cv2.VideoCapture(0)  # Initialize webcam
    
#     def process_video():
#         global video_capture
#         success, frame = video_capture.read()  # Capture a frame
#         if success:
#             frame = imutils.resize(frame, width=640)  # Resize frame if needed
#             play(source='video', frame=frame)  # Call play function with captured frame
            
#             # Schedule the next frame capture
#             lvideo.after(1, process_video)
    
#     process_video()


def capture():
    global filename, video_capture
    root = Tk()
    root.withdraw()
    fin =filedialog.askopenfilename()

    if fin:
        filename.set(fin)  # Set the file path to the filename variable
        print(fin)
        video_capture = cv2.VideoCapture(fin)  # Initialize video capture with the selected video file

        def process_video():
            global video_capture
            success, frame = video_capture.read()  # Capture a frame from the video file
            if success:
                frame = imutils.resize(frame, width=640)  # Resize frame if needed
                play(source='video', frame=frame)  # Call play function with captured frame
                
                # Schedule the next frame capture after a short delay
                lvideo.after(1, process_video)
            else:
                # Release the video capture when done or if there are no more frames
                video_capture.release()
                print("Video processing completed.")
        
        process_video()
         


def Start():
    global success
    success = True
    print('I am in Start')

    capture()
	
def Stop():
    global success
    success = False
    cv2.destroyAllWindows()
    tk.destroy()
    print('I am in Stop')


#GETTING THE FILE PATH
#print('number of frames not detected {}'.format(ncount))
#print('Total number of frames {}'.format(tcount))
filename=StringVar()
# filename = None
fin=' '
video_capture = None  
lb10 = None  
lvideo = None  
cap = None
def browse():
    global filename
    root = Tk()
    root.withdraw()
    fin =filedialog.askopenfilename()
    filename.set(fin)
    print(fin)
    play(source='image')

def play(source='image', frame=None):
    global lb10  # Global label for display

    if source == 'image':
        image_path = filename.get()  # Get the image path
        if image_path == '':
            browse()  # Open file dialog if no image selected
            return
        
        print(f"Processing image: {image_path}")
        image = cv2.imread(image_path)  # Read the selected image
    elif source == 'video':
        if frame is not None:
            image = frame  # Use the captured frame directly
        else:
            print("No frame captured.")
            return


    results = model_roboflow_agumentation(image)
    result = results[0]

    class_counts = {}
    if result.boxes is not None:
        for box in result.boxes:
            class_id = int(box.cls)
            class_name = model_roboflow_agumentation.names[class_id]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
            
            x1, y1, x2, y2 = box.xyxy[0] 

       
            x_center = int((x1 + x2) / 2)
            y_center = int((y1 + y2) / 2)

        
            cv2.drawMarker(image, (x_center, y_center), color=(0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)


    annotated_img_resized = cv2.resize(image, (667, 400))

    
    cv2image = cv2.cvtColor(annotated_img_resized, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)

  
    lvideo.imgtk = imgtk
    lvideo.configure(image=imgtk, width=667, height=400)

    object_description = ', '.join(f"{cls}: {count}" for cls, count in class_counts.items())
    if lb10 is not None:
        lb10.config(text=f"Detected: {object_description}")
    else:
        lb10 = Label(frame_2, width="24", height="10", text=f"Detected {object_description}", wraplength=200, borderwidth=4, relief="groove", bg="grey", font="Verdana 14 bold")
        lb10.place(x=9, y=250)

    print('Processing complete.')
    

                                    ############# the best code with bounding boxes #############################
# def play(source='image', frame=None):
#     global lb10  # Global label for display
    
#     if source == 'image':
#         image_path = filename.get()  # Get the image path
#         if image_path == '':
#             browse()  # Open file dialog if no image selected
#             return
        
#         print(f"Processing image: {image_path}")
#         image = cv2.imread(image_path)  # Read the selected image
#     elif source == 'video':
#         if frame is not None:
#             image = frame  # Use the captured frame directly
#         else:
#             print("No frame captured.")
#             return

#     # Detect objects using the model without manual resizing or normalization
#     results = model_roboflow_agumentation(image)  # Directly pass the loaded image
#     result = results[0]

#     # Check if detections exist
#     class_counts = {}
#     if result.boxes is not None:
#         # Iterate over detected boxes and count class occurrences
#         for box in result.boxes:
#             class_id = int(box.cls)  # Assuming box.cls contains class ID
#             class_name = model_roboflow_agumentation.names[class_id]
#             class_counts[class_name] = class_counts.get(class_name, 0) + 1
#     else:
#         # If no detections are found, print message
#         print("No detections found.")

#     # Plot and display detections using result.plot()
#     annotated_img = result.plot()
#     annotated_img_resized = cv2.resize(annotated_img, (667, 400))  # Resize for display in GUI

#     # Convert processed image for display in Tkinter
#     cv2image = cv2.cvtColor(annotated_img_resized, cv2.COLOR_BGR2RGBA)
#     img = Image.fromarray(cv2image)
#     imgtk = ImageTk.PhotoImage(image=img)

#     # Update the image display on the GUI
#     lvideo.imgtk = imgtk
#     lvideo.configure(image=imgtk, width=667, height=400)

#     # Create a description for each class count
#     object_description = ', '.join(f"{cls}: {count}" for cls, count in class_counts.items())

#     # Update or create a label for the object description
#     if lb10 is not None:
#         lb10.config(text=f"Detected: {object_description}")  # Update label if it exists
#     else:
#         lb10 = Label(frame_2, width="30", height="10", text=f"Detected: {object_description}", wraplength=200, borderwidth=4, relief="groove", bg="grey", font="Verdana 10 bold")
#         lb10.place(x=10, y=250)  # Place the label on the GUI

#     print('Processing complete.')

                        #################### ---------------------- ####################









    

#DATABASE CONNECTION

#client=MongoClient() 
#mydatabase = client['VB_TargetTracking'] 
#mycollection=mydatabase['Tracking_details'] 


tk.title("Object Counting App")
tk.geometry("1024x768")
tk.configure(bg="grey")
#FRAME SPLIT
frame_1 = Frame(tk, width=700, height=450, borderwidth=2, relief="groove", bg="grey")
frame_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

frame_2 = Frame(tk, width=300, height=400, borderwidth=2, relief="groove", bg="grey")
frame_2.grid(row=0, column=1, rowspan=2, padx=(0, 10), pady=10, sticky="nsew")

frame_3 = Frame(tk, width=708, height=200, borderwidth=2, relief="groove", bg="grey")
frame_3.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

# frame_1.grid(row=0,column=0)

# frame_3.grid(row=1,column=0,sticky=N+W)
# #frame_3.grid(sticky=N+W)
# frame_2.grid(rowspan=2)
# frame_2.grid(row=0,column=1,sticky=N+S)
'''

#image-list
lb9=Label(frame_2,width="44",height="3",text="Target Presence",borderwidth=2,relief="groove",bg="grey").place(x=300,y=80)

mylist=Listbox(frame_2,width=53,height=34)
mylist.place(x=300,y=145)
scrollbar = Scrollbar(tk,orient="vertical")
scrollbar.place(x=1332,y=148)
mylist.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=mylist.yview)

'''

#left-downfrom-fram-3
lb6=Label(frame_3,width="92",height="3",text="Image Upload",borderwidth=2,relief="groove",bg="grey").place(x=20,y=20)

lb5=Label(frame_3,width="20",height="2",text="Image path",borderwidth=2,relief="groove",bg="grey").place(x=20,y=100)
e4=Entry(frame_3,textvariable=filename,width=30,borderwidth=3).place(x=230,y=110)

bt2=Button(frame_3,text="Browse",width="13",relief="raised",borderwidth=4,command=browse,bg="grey").place(x=520,y=110)

#bt_play=Button(frame_3,text="Count",width="13",relief="raised",borderwidth=4,command=play,bg="grey").place(x=500,y=135)


#bt2=Button(frame_1,text="Capture",relief="raised",borderwidth=4,bg="grey")



frame_5=Frame(frame_1,width="700",height="400",padx=10,pady=10,borderwidth=4,relief="groove",bg="black")
frame_5.pack()
lvideo=Label(frame_5,width="95",height="27",borderwidth=4,relief="groove",bg="black")
lvideo.grid(sticky=S+W+E+N)
bt1=Button(frame_1,text="Capture",relief="raised",borderwidth=4,command=Start,bg="grey")
#bt1.grid(sticky=S)
bt1.pack(side=LEFT,ipadx=10,pady=10)
bt2=Button(frame_1,text="Stop",relief="raised",borderwidth=4,command=Stop,bg="grey")
#bt1.grid(sticky=S)
bt2.pack(side=RIGHT,ipadx=10,pady=10)


'''
lb1=Label(frame_2,width="93",height="3",text="Target Details",borderwidth=2,relief="groove",bg="grey")
lb1.grid(pady=5)

lb2=Label(frame_2,width="13",height="2",text="Target Name",borderwidth=2,relief="groove",bg="grey")
lb2.grid(padx=5,pady=12,sticky=W)

lb3=Label(frame_2,width="13",height="2",text="Target ID",borderwidth=2,relief="groove",bg="grey")
lb3.grid(padx=5,pady=12,sticky=W)

lb4=Label(frame_2,width="13",height="2",text="Date and Time",borderwidth=2,relief="groove",bg="grey")
lb4.grid(padx=5,pady=12,sticky=W)

#frame2-buttons
def AddEntry():
    rec={
    "Target_ID":3,
    "Target_Name":"Mr.XYZ",
    "Date_Time":"10/17/2019"
    }
    rec1 = mydatabase.Tracking_details.insert_one(rec)
    
    
#T_ID=StringVar
T_Name=StringVar
T_DT=StringVar

def Retrieve():
    rec2=mydatabase.Tracking_details.find({"Target_ID":1})
    for i in rec2:
        a=i["Target_ID"]
        b=i["Target_Name"]
        c=i["Date_Time"]
    
    #e1.insert(0,a)
    print(i)

    
    
def delete():
    mydatabase.Tracking_details.delete_one({"Target_ID":3})
    print("------------------Action-----------------")
    print("\nRecord deleted!!")

#INSERT UPDATE RETRIEVE DELETE
   
bt4=Button(frame_2,text="Add_Entry",width="12",relief="raised",borderwidth=4,command=AddEntry,bg="grey").place(x=25,y=500)
bt5=Button(frame_2,text="Retrieve",width="12",relief="raised",command=Retrieve,borderwidth=4,bg="grey").place(x=140,y=500)

bt6=Button(frame_2,text="Update",width="12",relief="raised",borderwidth=4,bg="grey").place(x=25,y=600)
bt7=Button(frame_2,text="Delete_Entry",width="12",relief="raised",command=delete,borderwidth=4,bg="grey").place(x=140,y=600)



#Textbox portion
e1=Entry(frame_2,width=20,borderwidth=3).place(x=110,y=81)
e2=Entry(frame_2,width=20,borderwidth=3).place(x=110,y=138)
e3=Entry(frame_2,width=20,borderwidth=3).place(x=110,y=199)
'''
tk.mainloop()
