# hsiao
import torch
from PIL import Image, ImageDraw, ImageFont
import random
import os


# People detection in single photo
def head_count(img_path="", hc_save_img=False):
    # Model
    model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

    # 確認img_path存在
    if os.path.isfile(img_path):
        if img_path.endswith((".jpg", ".png", ".jpeg", ".JPG")):

            # 檔名+副檔名
            img_name = os.path.basename(img_path)

            # 进行物体检测
            results = model(img_path)

            # 读取图像
            img = Image.open(img_path)

            # 调整绘图参数
            draw = ImageDraw.Draw(img)
            line_width = 5  # 修改此参数以更改边框线条宽度
            font_size = 50  # 修改此参数以更改字体大小

            # 定义一个字典将类别索引映射到随机颜色
            class_colors = {}
            for class_index in range(len(results.names)):
                class_colors[class_index] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                # 初始化一个ImageDraw对象
            # 初始化一个ImageDraw对象
            draw = ImageDraw.Draw(img)

            # 计算图像的宽度和高度
            image_width, image_height = img.size

            # 计算图像的中心坐标
            image_center_x = image_width / 2
            image_center_y = image_height / 2

            # 绘制红色长方形
            square_width = image_width * 0.7  # 将宽度设置为图像宽度的40%
            square_height = image_height  # 保持高度为图像的高度
            square_half_width = square_width / 2
            square_half_height = square_height / 2
            square_left = image_center_x - square_half_width
            square_top = image_center_y - square_half_height
            square_right = image_center_x + square_half_width
            square_bottom = image_center_y + square_half_height

            draw.rectangle((square_left, square_top, square_right, square_bottom), outline=(255, 0, 0),
                           width=line_width)

            # 初始化计数
            item_count = 0
            person_count = 0
            chair_count = 0

            # 遍历检测到的物体并绘制边界框
            for det in results.pred[0]:
                if det is not None and det[4] > 0.2:  # 根据置信度过滤检测结果
                    class_index = int(det[5])  # 提取类别索引
                    bbox = det[0:4].tolist()
                    bbox_width = bbox[2] - bbox[0]
                    bbox_height = bbox[3] - bbox[1]

                    # 计算物体的面积
                    object_area = bbox_width * bbox_height

                    if bbox[2] >= square_left and bbox[0] <= square_right and bbox[3] >= square_top and bbox[
                        1] <= square_bottom:
                        # 检测结果在红色长方形内，且面积大于3400
                        if object_area > 3400:
                            if results.names[class_index] == "suitcase" and det[4] > 0.4:
                                item_count += 1
                            elif results.names[class_index] == "person":
                                person_count += 1
                            elif results.names[class_index] == "chair" and det[4] > 0.3:
                                chair_count += 1
                            # 绘制边界框
                            draw.rectangle(bbox, outline=class_colors[class_index], width=line_width)
                            font = ImageFont.truetype("arial.ttf", font_size)  # 可能需要指定字体文件的路径
                            class_label = results.names[class_index]  # 使用检测结果中的类别名称
                            confidence = round(float(det[4]), 2)  # 提取置信度并将其四舍五入为2位小数
                            text = f'{class_label} ({confidence})\n'
                            text += f'宽度: {bbox_width:.2f}\n'
                            text += f'高度: {bbox_height:.2f}\n'
                            draw.text((bbox[0], bbox[1]), text, fill=class_colors[class_index], font=font)

            # 计算总物体数量
            total_objects = item_count * 0.5 + person_count

            # 计算总物体数量
            total_objects = item_count * 0.5 + person_count

            # 根据总数确定拥挤程度
            congestion_level = 0
            if total_objects <= 10 or chair_count > 0:
                congestion_level = 1
            elif 10 < total_objects <= 14 and (total_objects <= 15 or total_objects * object_area >= 33350):
                congestion_level = 2
            elif total_objects > 14:
                congestion_level = 3
            else:
                congestion_level = 0

            all_result = {
                img_name: {
                    "item_count": item_count,
                    "person_count": person_count,
                    "total_objects": total_objects,
                    "hc_congestion_level": congestion_level
                }
            }
            # print("item_count:", item_count)
            # print("person_count:", person_count)
            # print("total_objects:", total_objects)
            # print("level:", congestion_level)
            # print("\n")

            # 在图像上添加拥挤程度标签
            font = ImageFont.truetype("arial.ttf", font_size)  # 可能需要指定字体文件的路径
            text = f'total: {total_objects} | item_count: {item_count} | person_count: {person_count}\n{congestion_level}'  # 在标签中包含总物体数和拥挤程度
            draw.text((10, 10), text, fill=(255, 255, 255), font=font)  # 根据需要调整位置和填充颜色

            if hc_save_img is True:
                output_dir = 'examples/res/vis_head_count'
                # 保存修改后的图像到输出目录
                output_path = os.path.join(output_dir, img_name)
                img.save(output_path)

            return 1, all_result
        else:
            return 0, "The file is not image."
    else:
        return 0, "You don't input image path."


# People detection in multiple photos: version 2
def head_count_in_multi(input_dir="", hc_save_img=False):
    # Model
    model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

    # final return
    all_result = {}

    # 確認img_path存在
    if os.path.isdir(input_dir):
        # 遍历输入目录中的所有图像文件
        for filename in os.listdir(input_dir):
            if filename.endswith((".jpg", ".png", ".jpeg", ".JPG")):
                # 构建图像文件的完整路径
                img_path = os.path.join(input_dir, filename)

                # 檔名+副檔名
                img_name = os.path.basename(img_path)

                # 进行物体检测
                results = model(img_path)

                # 读取图像
                img = Image.open(img_path)

                # 调整绘图参数
                draw = ImageDraw.Draw(img)
                line_width = 5  # 修改此参数以更改边框线条宽度
                font_size = 50  # 修改此参数以更改字体大小

                # 定义一个字典将类别索引映射到随机颜色
                class_colors = {}
                for class_index in range(len(results.names)):
                    class_colors[class_index] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    # 初始化一个ImageDraw对象
                # 初始化一个ImageDraw对象
                draw = ImageDraw.Draw(img)

                # 计算图像的宽度和高度
                image_width, image_height = img.size

                # 计算图像的中心坐标
                image_center_x = image_width / 2
                image_center_y = image_height / 2

                # 绘制红色长方形
                square_width = image_width * 0.7  # 将宽度设置为图像宽度的40%
                square_height = image_height  # 保持高度为图像的高度
                square_half_width = square_width / 2
                square_half_height = square_height / 2
                square_left = image_center_x - square_half_width
                square_top = image_center_y - square_half_height
                square_right = image_center_x + square_half_width
                square_bottom = image_center_y + square_half_height

                draw.rectangle((square_left, square_top, square_right, square_bottom), outline=(255, 0, 0),
                               width=line_width)

                # 初始化计数
                item_count = 0
                person_count = 0
                chair_count = 0
                object_area = 0

                # 遍历检测到的物体并绘制边界框
                for det in results.pred[0]:
                    if det is not None and det[4] > 0.2:  # 根据置信度过滤检测结果
                        class_index = int(det[5])  # 提取类别索引
                        bbox = det[0:4].tolist()
                        bbox_width = bbox[2] - bbox[0]
                        bbox_height = bbox[3] - bbox[1]

                        # 计算物体的面积
                        object_area = bbox_width * bbox_height

                        if bbox[2] >= square_left and bbox[0] <= square_right and bbox[3] >= square_top and bbox[
                            1] <= square_bottom:
                            # 检测结果在红色长方形内，且面积大于3400
                            if object_area > 3400:
                                if results.names[class_index] == "suitcase" and det[4] > 0.4:
                                    item_count += 1
                                elif results.names[class_index] == "person":
                                    person_count += 1
                                elif results.names[class_index] == "chair" and det[4] > 0.3:
                                    chair_count += 1
                                # 绘制边界框
                                draw.rectangle(bbox, outline=class_colors[class_index], width=line_width)
                                font = ImageFont.truetype("arial.ttf", font_size)  # 可能需要指定字体文件的路径
                                class_label = results.names[class_index]  # 使用检测结果中的类别名称
                                confidence = round(float(det[4]), 2)  # 提取置信度并将其四舍五入为2位小数
                                text = f'{class_label} ({confidence})\n'
                                text += f'宽度: {bbox_width:.2f}\n'
                                text += f'高度: {bbox_height:.2f}\n'
                                draw.text((bbox[0], bbox[1]), text, fill=class_colors[class_index], font=font)

                # 计算总物体数量
                total_objects = item_count * 0.5 + person_count

                # 计算总物体数量
                total_objects = item_count * 0.5 + person_count

                # 根据总数确定拥挤程度
                congestion_level = 0
                if total_objects <= 10 or chair_count > 0:
                    congestion_level = 1
                elif 10 < total_objects <= 14 and (total_objects <= 15 or total_objects * object_area >= 33350):
                    congestion_level = 2
                elif total_objects > 14:
                    congestion_level = 3
                else:
                    congestion_level = 0

                all_result[img_name] = {
                    "item_count": item_count,
                    "person_count": person_count,
                    "chair_count": chair_count,
                    "total_objects": total_objects,
                    "hc_congestion_level": congestion_level
                }

                # print("item_count:", item_count)
                # print("person_count:", person_count)
                # print("total_objects:", total_objects)
                # print("level:", congestion_level)
                # print("\n")

                # 在图像上添加拥挤程度标签
                font = ImageFont.truetype("arial.ttf", font_size)  # 可能需要指定字体文件的路径
                text = f'total: {total_objects} | item_count: {item_count} | person_count: {person_count}\n{congestion_level}'  # 在标签中包含总物体数和拥挤程度
                draw.text((10, 10), text, fill=(255, 255, 255), font=font)  # 根据需要调整位置和填充颜色

                if hc_save_img is True:
                    output_dir = 'examples/res/vis_head_count'
                    # 保存修改后的图像到输出目录
                    output_path = os.path.join(output_dir, img_name)
                    img.save(output_path)

            else:
                return 0, "The file is not image."

        return 1, all_result
    else:
        return 0, "You don't input image path."


# People detection in single photo: version 1
def head_count_v1(img_path="", hc_save_img=False):
    # Model
    model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

    # 確認img_path存在
    if os.path.isfile(img_path):
        if img_path.endswith((".jpg", ".png", ".jpeg", ".JPG")):

            # 檔名+副檔名
            img_name = os.path.basename(img_path)

            # 进行物体检测
            results = model(img_path)

            # 读取图像
            img = Image.open(img_path)

            # 调整绘图参数
            draw = ImageDraw.Draw(img)
            line_width = 3  # 修改此参数以更改边框线条宽度
            font_size = 20  # 修改此参数以更改字体大小

            # 定义一个字典将类别索引映射到随机颜色
            class_colors = {}
            for class_index in range(len(results.names)):
                class_colors[class_index] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # 获取图像的宽度和高度
            img_width, img_height = img.size

            # 定义中心区域的水平范围
            center_x_min = (img_width // 2) - 575  # 中心区域左边界
            center_x_max = (img_width // 2) + 575  # 中心区域右边界
            # 初始化计数
            item_count = 0
            person_count = 0

            # 迭代检测到的物体并绘制边界框
            for det in results.pred[0]:
                if det is not None and det[4] > 0.2:  # 根据置信度过滤检测结果
                    class_index = int(det[5])  # 提取类别索引
                    bbox = det[0:4].tolist()
                    bbox_width = bbox[2] - bbox[0]
                    bbox_height = bbox[3] - bbox[1]

                    object_center_x = (bbox[0] + bbox[2]) / 2

                    # 根据宽度和高度门限过滤太小或太远的物体
                    if bbox_width * bbox_height >= 0:
                        if results.names[class_index] == "suitcase" and det[4] > 0.4:
                            item_count += 1
                            # 绘制边界框
                            draw.rectangle(bbox, outline=class_colors[class_index], width=line_width)
                            font = ImageFont.truetype("arial.ttf", font_size)  # 可能需要指定字体文件的路径
                            class_label = results.names[class_index]  # 使用检测结果中的类别名称
                            confidence = round(float(det[4]), 2)  # 提取置信度并将其四舍五入为2位小数
                            text = f'{class_label} ({confidence})\n'
                            text += f'宽度: {bbox_width:.2f}\n'
                            text += f'高度: {bbox_height:.2f}\n'
                            draw.text((bbox[0], bbox[1]), text, fill=class_colors[class_index], font=font)
                        elif results.names[class_index] == "person" and not (
                            bbox_width * bbox_height <= 27500 and center_x_min <= object_center_x <= center_x_max):
                            person_count += 1
                            # 绘制边界框
                            draw.rectangle(bbox, outline=class_colors[class_index], width=line_width)
                            font = ImageFont.truetype("arial.ttf", font_size)  # 可能需要指定字体文件的路径
                            class_label = results.names[class_index]  # 使用检测结果中的类别名称
                            confidence = round(float(det[4]), 2)  # 提取置信度并将其四舍五入为2位小数
                            text = f'{class_label} ({confidence})\n'
                            text += f'宽度: {bbox_width:.2f}\n'
                            text += f'高度: {bbox_height:.2f}\n'
                            draw.text((bbox[0], bbox[1]), text, fill=class_colors[class_index], font=font)

            # 计算总物体数量
            total_objects = item_count + person_count

            # 根据总数确定拥挤程度
            congestion_level = ""
            if total_objects <= 10:
                congestion_level = 1
            elif 10 < total_objects <= 13:
                congestion_level = 2
            else:
                congestion_level = 3

            if results.names[class_index] == "bench":
                congestion_level = 1
            if results.names[class_index] == "chair" and det[4] > 0.4:
                congestion_level = 1

            all_result = {
                img_name: {
                    "item_count": item_count,
                    "person_count": person_count,
                    "total_objects": total_objects,
                    "hc_congestion_level": congestion_level
                }
            }
            # print("item_count:", item_count)
            # print("person_count:", person_count)
            # print("total_objects:", total_objects)
            # print("level:", congestion_level)
            # print("\n")

            # 在图像上添加拥挤程度标签
            font = ImageFont.truetype("arial.ttf", font_size)  # 可能需要指定字体文件的路径
            text = f'total: {total_objects} | item_count: {item_count} | person_count: {person_count}\n{congestion_level}'  # 在标签中包含总物体数和拥挤程度
            draw.text((10, 10), text, fill=(255, 255, 255), font=font)  # 根据需要调整位置和填充颜色

            if hc_save_img is True:
                output_dir = 'examples/res/vis_head_count'
                # 保存修改后的图像到输出目录
                output_path = os.path.join(output_dir, img_name)
                img.save(output_path)

            return 1, all_result
        else:
            return 0, "The file is not image."
    else:
        return 0, "You don't input image path."


# People detection in multiple photos: version 1
def head_count_in_multi_v1(input_dir="", hc_save_img=False):
    # Model
    model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

    # final return
    all_result = {}

    # 確認img_path存在
    if os.path.isdir(input_dir):
        # 遍历输入目录中的所有图像文件
        for filename in os.listdir(input_dir):
            if filename.endswith((".jpg", ".png", ".jpeg", ".JPG")):
                # 构建图像文件的完整路径
                img_path = os.path.join(input_dir, filename)

                # 檔名+副檔名
                img_name = os.path.basename(img_path)

                # 进行物体检测
                results = model(img_path)

                # 读取图像
                img = Image.open(img_path)

                # 调整绘图参数
                draw = ImageDraw.Draw(img)
                line_width = 3  # 修改此参数以更改边框线条宽度
                font_size = 20  # 修改此参数以更改字体大小

                # 定义一个字典将类别索引映射到随机颜色
                class_colors = {}
                for class_index in range(len(results.names)):
                    class_colors[class_index] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                # 获取图像的宽度和高度
                img_width, img_height = img.size

                # 定义中心区域的水平范围
                center_x_min = (img_width // 2) - 575  # 中心区域左边界
                center_x_max = (img_width // 2) + 575  # 中心区域右边界
                # 初始化计数
                item_count = 0
                person_count = 0

                # 迭代检测到的物体并绘制边界框
                for det in results.pred[0]:
                    if det is not None and det[4] > 0.2:  # 根据置信度过滤检测结果
                        class_index = int(det[5])  # 提取类别索引
                        bbox = det[0:4].tolist()
                        bbox_width = bbox[2] - bbox[0]
                        bbox_height = bbox[3] - bbox[1]

                        object_center_x = (bbox[0] + bbox[2]) / 2

                        # 根据宽度和高度门限过滤太小或太远的物体
                        if bbox_width * bbox_height >= 0:
                            if results.names[class_index] == "suitcase" and det[4] > 0.4:
                                item_count += 1
                                # 绘制边界框
                                draw.rectangle(bbox, outline=class_colors[class_index], width=line_width)
                                font = ImageFont.truetype("arial.ttf", font_size)  # 可能需要指定字体文件的路径
                                class_label = results.names[class_index]  # 使用检测结果中的类别名称
                                confidence = round(float(det[4]), 2)  # 提取置信度并将其四舍五入为2位小数
                                text = f'{class_label} ({confidence})\n'
                                text += f'宽度: {bbox_width:.2f}\n'
                                text += f'高度: {bbox_height:.2f}\n'
                                draw.text((bbox[0], bbox[1]), text, fill=class_colors[class_index], font=font)
                            elif results.names[class_index] == "person" and not (
                                bbox_width * bbox_height <= 27500 and center_x_min <= object_center_x <= center_x_max):
                                person_count += 1
                                # 绘制边界框
                                draw.rectangle(bbox, outline=class_colors[class_index], width=line_width)
                                font = ImageFont.truetype("arial.ttf", font_size)  # 可能需要指定字体文件的路径
                                class_label = results.names[class_index]  # 使用检测结果中的类别名称
                                confidence = round(float(det[4]), 2)  # 提取置信度并将其四舍五入为2位小数
                                text = f'{class_label} ({confidence})\n'
                                text += f'宽度: {bbox_width:.2f}\n'
                                text += f'高度: {bbox_height:.2f}\n'
                                draw.text((bbox[0], bbox[1]), text, fill=class_colors[class_index], font=font)

                # 计算总物体数量
                total_objects = item_count + person_count

                # 根据总数确定拥挤程度
                congestion_level = ""
                if total_objects <= 10:
                    congestion_level = 1
                elif 10 < total_objects <= 13:
                    congestion_level = 2
                else:
                    congestion_level = 3

                if results.names[class_index] == "bench":
                    congestion_level = 1
                if results.names[class_index] == "chair" and det[4] > 0.4:
                    congestion_level = 1

                all_result[img_name] = {
                    "item_count": item_count,
                    "person_count": person_count,
                    "total_objects": total_objects,
                    "hc_congestion_level": congestion_level
                }

                # print("item_count:", item_count)
                # print("person_count:", person_count)
                # print("total_objects:", total_objects)
                # print("level:", congestion_level)
                # print("\n")

                # 在图像上添加拥挤程度标签
                font = ImageFont.truetype("arial.ttf", font_size)  # 可能需要指定字体文件的路径
                text = f'total: {total_objects} | item_count: {item_count} | person_count: {person_count}\n{congestion_level}'  # 在标签中包含总物体数和拥挤程度
                draw.text((10, 10), text, fill=(255, 255, 255), font=font)  # 根据需要调整位置和填充颜色

                if hc_save_img is True:
                    output_dir = 'examples/res/vis_head_count'
                    # 保存修改后的图像到输出目录
                    output_path = os.path.join(output_dir, img_name)
                    img.save(output_path)

            else:
                return 0, "The file is not image."

        return 1, all_result
    else:
        return 0, "You don't input image path."
