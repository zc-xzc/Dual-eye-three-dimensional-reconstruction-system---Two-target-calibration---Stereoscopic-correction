def get_rectify_image(self, imgL, imgR):
    """
    畸变校正和立体校正
    根据更正map对图片进行重构
    获取用于畸变校正和立体校正的映射矩阵以及用于计算像素空间坐标的重投影矩阵
    :param imgL:
    :param imgR:
    :return:
    """
    # camera_params.get_rectify_transform(K1, D1, K2, D2, R, T, image_size)
    left_map_x, left_map_y = self.camera_config["left_map_x"], self.camera_config["left_map_y"]
    right_map_x, right_map_y = self.camera_config["right_map_x"], self.camera_config["right_map_y"]
    rectifiedL = cv2.remap(imgL, left_map_x, left_map_y, cv2.INTER_LINEAR, borderValue=cv2.BORDER_CONSTANT)
    rectifiedR = cv2.remap(imgR, right_map_x, right_map_y, cv2.INTER_LINEAR, borderValue=cv2.BORDER_CONSTANT)
    return rectifiedL, rectifiedR