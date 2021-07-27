from argparse import ArgumentParser

import cv2

from mmtrack.apis import inference_sot, init_model


def main():


    # build the model from a config file and a checkpoint file
    model = init_model("../../../excellentDependency/mmtracking/configs/sot/siamese_rpn/siamese_rpn_r50_1x_lasot.py","../../../resources/modelWeights/siamese_rpn_r50_1x_lasot_20201218_051019-3c522eff.pth", device="cuda:0")

    # input="C://Users/24225/Downloads/test02.mp4"
    cap = cv2.VideoCapture(0)


    frame_id = 0
    while (cap.isOpened()):
        flag, frame = cap.read()
        if not flag:
            break

        if frame_id == 0:
            init_bbox = list(cv2.selectROI('SOT_NAME', frame, False, False))
            # convert (x1, y1, w, h) to (x1, y1, x2, y2)
            init_bbox[2] += init_bbox[0]
            init_bbox[3] += init_bbox[1]

        # test a single image
        result = inference_sot(model, frame, init_bbox, frame_id)

        track_bbox = result['bbox']
        vis_frame = model.show_result(
            frame,
            track_bbox,
            color=(0,255,0),
            thickness=3,
            show=False)

        cv2.imshow("test",vis_frame)



        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_id = 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
