import StringIO

import angus
import cv2
import numpy as np

if __name__ == '__main__':    
    ### Web cam index might be different from 0 on your setup.
    stream_index = 0 
    cap = cv2.VideoCapture(stream_index)

    if not cap.isOpened():
        print "Cannot open stream of index " + str(stream_index)
        exit(1)

    print "Video stream is of resolution " + str(cap.get(3)) + " x " + str(cap.get(4))

    conn = angus.connect()
    service = conn.services.get_service("age_and_gender_estimation", version=1)
    service.enable_session()

    while(cap.isOpened()):
        ret, frame = cap.read()
        if not frame == None:

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, buff = cv2.imencode(".png", gray)
            buff = StringIO.StringIO(np.array(buff).tostring())

            job = service.process({"image": buff})
            res = job.result

            if res['nb_faces'] > 0:
                for i in range(0,res['nb_faces']):
                    roi = res['faces'][i]['roi']
                    cv2.rectangle(frame, (int(roi[0]), int(roi[1])), 
                                         (int(roi[0] + roi[2]), int(roi[1] + roi[3])), 
                                         (0,255,0))
                    age = res['faces'][i]['age']
                    gender = res['faces'][i]['gender']
                    cv2.putText(frame, "(age, gender) = (" + '%.1f'%age + ", " + str(gender) + ")", 
                                (int(roi[0]), int(roi[1])), cv2.FONT_HERSHEY_SIMPLEX, 
                                0.8, (255, 255, 255))


            cv2.imshow('original', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    service.disable_session()

    cap.release()
    cv2.destroyAllWindows()