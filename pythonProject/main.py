import cv2
import streamlit as st
import numpy as np
from PIL import Image

def cartoonization (image, cartoon):
    # 将图像转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if cartoon == "铅笔素描":
        value = st.sidebar.slider('调整草图的亮度（值越高，草图越亮）',
                                  0.0, 300.0, 250.0)
        kernel = st.sidebar.slider(
            '调整草图边缘的大胆程度（值越高，边缘越大胆）', 1, 99, 25,
            step=2)

        # 使用高斯模糊平滑图像
        blurred_image = cv2.GaussianBlur(gray_image, (kernel, kernel), 0)

        # 将图像转换为铅笔草图
        cartoon = cv2.divide(gray_image, blurred_image, scale=value)

    if cartoon == "细节增强":
        smooth = st.sidebar.slider(
            '调整图像的平滑度（值越高，图像越平滑）', 3, 99, 5, step=2)
        kernel = st.sidebar.slider('调整图像的清晰度（值越低，图像越清晰）', 1, 21, 3,
                                   step=2)
        edge_preserve = st.sidebar.slider(
            '调整颜色平均效果（低：仅平滑相似的颜色，高：平滑不同的颜色）',
            0.0, 1.0, 0.5)

        # 使用中值模糊平滑图像
        blurred_image = cv2.medianBlur(gray_image, kernel)

        # 利用自适应阈值来检测边缘
        edges_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)

        # 锐化图像
        color_image = cv2.detailEnhance(image, sigma_s=smooth, sigma_r=edge_preserve)

        # 使用“边”作为遮罩合并相同图像的颜色
        cartoon = cv2.bitwise_and(color_image, color_image, mask=edges_image)

    if cartoon == "双边滤波器":
        smooth = st.sidebar.slider(
            '调整图像的平滑度（值越高，图像越平滑）', 3, 99, 5, step=2)
        kernel = st.sidebar.slider('调整图像的清晰度（值越低，图像越清晰）', 1, 21, 3,
                                   step=2)
        edge_preserve = st.sidebar.slider(
            '调整颜色平均效果（低：仅平滑相似的颜色，高：平滑不同的颜色）',
            1, 100, 50)

        # 使用中值模糊平滑图像
        blurred_image = cv2.medianBlur(gray_image, kernel)

        # 利用自适应阈值来检测边缘
        edges_image = cv2.adaptiveThreshold(blurred_image , 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)

        # 锐化图像
        color_image = cv2.bilateralFilter(image, smooth, edge_preserve, smooth)

        # 使用“边”作为遮罩合并相同图像的颜色
        cartoon = cv2.bitwise_and(color_image, color_image, mask=edges_image)

    if cartoon == "铅笔边缘":
        kernel = st.sidebar.slider('调整草图的清晰度（值越低，清晰度越高）', 1, 99,
                                   25, step=2)
        laplacian_filter = st.sidebar.slider(
            '调整边缘检测功率（值越高，功率越大）', 3, 9, 3, step=2)
        noise_reduction = st.sidebar.slider(
            '调整草图的噪波效果（值越高，噪波越大）', 10, 255, 150)

        # 使用中值模糊平滑图像
        blurred_image = cv2.medianBlur(gray_image, kernel)

        # 用拉普拉斯算子检测边缘
        edges_image = cv2.Laplacian(blurred_image, -1, ksize=laplacian_filter)

        # 反转边
        edges_image_inver = 255 - edges_image

        # 将图像转换为铅笔边缘草图
        dummy, cartoon = cv2.threshold(edges_image_inver, noise_reduction, 255, cv2.THRESH_BINARY)

    return cartoon

###############################################################################

st.write("""
          # 卡通化你的形象！

          """
          )

st.write("这是一个将你的照片变成卡通的应用程序")

file = st.sidebar.file_uploader("请上传图像文件", type=["jpg", "png"])

if file is None:
    st.text("您尚未上传图像文件")
else:
    image = Image.open(file)
    image = np.array(image)

    option = st.sidebar.selectbox(
        '你想应用哪些卡通滤镜？',
        ('铅笔素描', '细节增强', '铅笔边缘', '双边滤波器'))

    st.text("您的原始图像")
    st.image(image, use_column_width=True)

    st.text("你的卡通形象")
    cartoon = cartoonization(image, option)

    st.image(cartoon, use_column_width=True)