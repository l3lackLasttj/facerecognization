from flask import Flask, render_template, request, session, redirect, url_for, Response, jsonify
import mysql.connector
import cv2
from PIL import Image
import numpy as np
import os
import time
from datetime import date
import random
import psycopg2
import psycopg2.extras
import json


app = Flask(__name__)
camera = cv2.VideoCapture(0)
cnt = 0
pause_cnt = 0
justscanned = False

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="student_walailak_db"
)
mycursor = mydb.cursor()


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Generate dataset >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def generate_dataset(id):
    face_classifier = cv2.CascadeClassifier(
        "C:/Users/Admin/Desktop/faceRecognition_files/resources/haarcascade_frontalface_default.xml")

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        # scaling factor=1.3
        # Minimum neighbor = 5

        if faces is ():
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        return cropped_face

    cap = cv2.VideoCapture(0)

    mycursor.execute("select ifnull(max(img_id), 0) from img_dataset")
    row = mycursor.fetchone()
    lastid = row[0]

    img_id = lastid
    max_imgid = img_id + 100
    count_img = 0

    while True:
        ret, img = cap.read()
        if face_cropped(img) is not None:
            count_img += 1
            img_id += 1
            face = cv2.resize(face_cropped(img), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            file_name_path = "dataset/"+id+"." + str(img_id) + ".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(count_img), (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            mycursor.execute("""INSERT INTO `img_dataset` (`img_id`, `img_person`) VALUES
                                ('{}', '{}')""".format(img_id, id))
            mydb.commit()

            frame = cv2.imencode('.jpg', face)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            if cv2.waitKey(1) == 13 or int(img_id) == int(max_imgid):
                break
                cap.release()
                cv2.destroyAllWindows()


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Train Classifier >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/train_classifier/<id>')
def train_classifier(id):
    dataset_dir = "C:/Users/Admin/Desktop/faceRecognition_files/dataset"

    path = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)]
    faces = []
    ids = []

    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])

        faces.append(imageNp)
        ids.append(id)
    ids = np.array(ids)

    # Train the classifier and save
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("classifier.xml")

    return redirect('/')


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Face Recognition >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def face_recognition():  # generate frame by frame from camera
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(
            gray_image, scaleFactor, minNeighbors)

        global justscanned
        global pause_cnt

        pause_cnt += 1

        coords = []

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            if confidence > 70 and not justscanned:
                global cnt
                cnt += 1
                # สูตรในการหา
                n = (100 / 30) * cnt
                # w_filled = (n / 100) * w
                w_filled = (cnt / 30) * w

                cv2.putText(img, str(int(n))+' %', (x + 20, y + h + 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)

                cv2.rectangle(img, (x, y + h + 40),
                              (x + w, y + h + 50), color, 2)
                cv2.rectangle(img, (x, y + h + 40), (x + int(w_filled),
                              y + h + 50), (153, 255, 255), cv2.FILLED)

                mycursor.execute("select a.img_person, b.student_name, b.student_major, b.student_dormitory, b.student_room"
                                 "  from img_dataset a "
                                 "  left join student_information b on a.img_person = b.student_id "
                                 " where img_id = " + str(id))
                row = mycursor.fetchone()
                id = row[0]
                name = row[1]
                major = row[2]

                if int(cnt) == 30:
                    cnt = 0

                    mycursor.execute("insert into check_in (enter_date, enter_number) values('"+str(date.today())+"', '" + id + "')")
                    mydb.commit()

                    cv2.putText(img, name + ' | ' + major, (x - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)
                    time.sleep(1)

                    justscanned = True
                    pause_cnt = 0

            else:
                if not justscanned:
                    cv2.putText(img, 'UNKNOWN', (x, y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                    mycursor.execute("insert into unknow (createdAt) values('"+str(date.today())+"')")
                    mydb.commit()
                    # for i in range(10):
                    #return_value, image = camera.read()
                    #cv2.imwrite('unknow/'+str(random.sample(range(100), 10))+'.png', image)

                else:
                    cv2.putText(
                        img, ' ', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

                if pause_cnt > 80:
                    justscanned = False

            coords = [x, y, w, h]
        return coords

    def recognize(img, clf, faceCascade):
        coords = draw_boundary(img, faceCascade, 1.1, 10,
                               (255, 255, 0), "Face", clf)
        return img

    faceCascade = cv2.CascadeClassifier("C:/Users/Admin/Desktop/faceRecognition_files/resources/haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    wCam, hCam = 400, 400

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while True:
        ret, img = cap.read()
        img = recognize(img, clf, faceCascade)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break


def face_recognitionout():  # generate frame by frame from camera
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(
            gray_image, scaleFactor, minNeighbors)

        global justscanned
        global pause_cnt

        pause_cnt += 1

        coords = []

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            if confidence > 70 and not justscanned:
                global cnt
                cnt += 1
                # สูตรในการหา
                n = (100 / 30) * cnt
                # w_filled = (n / 100) * w
                w_filled = (cnt / 30) * w

                cv2.putText(img, str(int(n))+' %', (x + 20, y + h + 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)

                cv2.rectangle(img, (x, y + h + 40),
                              (x + w, y + h + 50), color, 2)
                cv2.rectangle(img, (x, y + h + 40), (x + int(w_filled),
                              y + h + 50), (153, 255, 255), cv2.FILLED)

                mycursor.execute("select a.img_person, b.student_name, b.student_major, b.student_dormitory, b.student_room"
                                 "  from img_dataset a "
                                 "  left join student_information b on a.img_person = b.student_id "
                                 " where img_id = " + str(id))
                row = mycursor.fetchone()
                id = row[0]
                name = row[1]
                major = row[2]

                if int(cnt) == 30:
                    cnt = 0

                    mycursor.execute("insert into check_out (out_date, out_number) values('"+str(date.today())+"', '" + id + "')")
                    mydb.commit()

                    cv2.putText(img, name + ' | ' + major, (x - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)
                    time.sleep(1)

                    justscanned = True
                    pause_cnt = 0

            else:
                if not justscanned:
                    cv2.putText(img, 'UNKNOWN', (x, y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                   # mycursor.execute("insert into unknow (createdAt) values('"+str(date.today())+"')")
                  #  mydb.commit()

                   # return_value, image = camera.read()
                   # cv2.imwrite('unknow/'+str(random.sample(range(1000000000), 10))+'.png', image)

                else:
                    cv2.putText(
                        img, ' ', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

                if pause_cnt > 80:
                    justscanned = False

            coords = [x, y, w, h]
        return coords

    def recognize(img, clf, faceCascade):
        coords = draw_boundary(img, faceCascade, 1.1, 10,
                               (255, 255, 0), "Face", clf)
        return img

    faceCascade = cv2.CascadeClassifier("C:/Users/Admin/Desktop/faceRecognition_files/resources/haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    wCam, hCam = 400, 400

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while True:
        ret, img = cap.read()
        img = recognize(img, clf, faceCascade)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break


@app.route('/')
def home():
    mycursor.execute("select student_id, student_name, student_major, student_dormitory, student_room, student_active, student_added from student_information")
    data = mycursor.fetchall()

    return render_template('index.html', data=data)


@app.route('/addstudent')
def addstudent():
    mycursor.execute("select ifnull(max(student_id) + 1, 101) from student_information")
    row = mycursor.fetchone()
    id = row[0]
    # print(int(id))

    return render_template('addstudent.html', newid=int(id))


@app.route('/addstudent_major', methods=['POST'])
def addstudent_major():
    studentid = request.form.get('txtid')
    studentname = request.form.get('txtname')
    studentmajor = request.form.get('major')
    studentdormitory = request.form.get('dormitory')
    studentroom = request.form.get('room')
    mycursor.execute("""INSERT INTO `student_information` (`student_id`, `student_name`, `student_major`, `student_dormitory`, `student_room`) VALUES
                    ('{}', '{}', '{}', '{}', '{}')""".format(studentid, studentname, studentmajor, studentdormitory, studentroom))
    mydb.commit()

    # return redirect(url_for('home'))
    return redirect(url_for('vfdataset_page', student=studentid))


@app.route('/vfdataset_page/<student>')
def vfdataset_page(student):
    return render_template('gendataset.html', student=student)


@app.route('/vidfeed_dataset/<id>')
def vidfeed_dataset(id):
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(generate_dataset(id), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(face_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feedout')
def video_feedout():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(face_recognitionout(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/check_in')
def check_in():
    """Video streaming home page."""
    mycursor.execute("select a.enter_id, a.enter_number, b.student_name, b.student_major, a.enter_added "
                     "  from check_in a "
                     "  left join student_information b on a.enter_number = b.student_id "
                     " where a.enter_date = curdate() "
                     " order by 1 desc")
    data = mycursor.fetchall()

    return render_template('check_in.html', data=data)


@app.route('/check_out')
def check_out():
    """Video streaming home page."""
    mycursor.execute("select a.out_id, a.out_number, b.student_name, b.student_major, a.out_added "
                     "  from check_out a "
                     "  left join student_information b on a.out_number = b.student_id "
                     " where a.out_date = curdate() "
                     " order by 1 desc")
    data = mycursor.fetchall()
    
    return render_template('check_out.html', data=data)


@app.route('/chkin')
def chkin():

    mycursor.execute("select count(*) "
                     "  from check_in "
                     " where enter_date = curdate() ")
    row = mycursor.fetchone()
    rowcount = row[0]

    return jsonify({'rowcount': rowcount})


@app.route('/chkout')
def chkout():

    mycursor.execute("select count(*) "
                     "  from check_out "
                     " where out_date = curdate() ")
    row = mycursor.fetchone()
    rowcount = row[0]

    return jsonify({'rowcount': rowcount})  # อาจจะผิด


@app.route('/loadData', methods=['GET', 'POST'])
def loadData():

    mycursor.execute("select a.enter_id, a.enter_number, b.student_name, b.student_major, date_format(a.enter_added, '%H:%i:%s') "
                     "  from check_in a "
                     "  left join student_information b on a.enter_number = b.student_id "
                     " where a.enter_date = curdate() "
                     " order by 1 desc")
    data = mycursor.fetchall()

    return jsonify(response=data)


@app.route('/loadDataOut', methods=['GET', 'POST'])
def loadDataOut():

    mycursor.execute("select a.out_id, a.out_number, b.student_name, b.student_major, date_format(a.out_added, '%H:%i:%s') "
                     "  from check_out a "
                     "  left join student_information b on a.out_number = b.student_id "
                     " where a.out_date = curdate() "
                     " order by 1 desc")
    data = mycursor.fetchall()

    return jsonify(response=data)


@app.route('/search')
def search():
    
    #cur = mydb.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #mycursor.execute("SELECT * FROM student_information ORDER BY student_id desc")
    mycursor.execute("SELECT student_id, student_name, student_major, student_room, student_added from student_information ORDER BY student_id")
    data = mycursor.fetchall()
    return render_template('search.html', data=data)


@app.route("/range", methods=["POST", "GET"])
def range():
    if request.method == 'Post':
        From = request.form['From']
        to = request.form['to']
        print('from : ', From)
        print('to : ', to)
        query = "SELECT * check_in.enter_date,student_information.student_name FROM `check_in` INNER JOIN student_information on check_in.enter_number = student_information.student_id BETWEEN '{}' AND '{}'".format(From, to)
        mycursor.execute(query)
        data = mycursor.fetchall()
    return jsonify({'htmlresponse': render_template('response.html', data=data)})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
