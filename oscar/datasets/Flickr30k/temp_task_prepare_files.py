# find the over lapping ids
# outout file
import os
import csv
import random
import sys
import json

csv.field_size_limit(sys.maxsize)

def prepare_fea_cap_od_files(id_set={},in_fea="features.tsv",out_fea="test_features.tsv",
        in_caption_csv="flickr_result_from_kaggle.csv",out_caption_json="test_flickr_caption.json",out_caption_coco_json="test_flickr_caption_coco_format.json",
        in_od="predictions.tsv",out_od="test_predictions.tsv"):
    # prepare feat
    with open(in_fea,'r') as in_f, open(out_fea,'w') as out_f:
        csv_reader = csv.reader(in_f,delimiter='\t')
        for line in csv_reader:
                id = line[0]
                if id in id_set:
                        out_f.write("\t".join(line)+"\n")
    # prepare caption
    result = []
    all_id = []
    with open(in_caption_csv,'r') as in_f,open(out_caption_json,'w') as out_f, open(out_caption_coco_json,'w') as out_f_c:
        for line in in_f.readlines():
            try:
                image_name,comment_number,comment = line.strip().split("|")
                image_id = image_name.replace(".jpg","").strip()
                if image_id not in id_set:
                    continue
                id = int(comment_number.strip()) # I assume comment number is id
                caption = comment.strip()
                result.append({"image_id":image_id,"id":id,"caption":caption})
                all_id.append({"id": str(image_id), "file_name": str(image_id)})
            except:
                print(line)

        result_coco = {"annotations": result,"images":all_id,"type":"captions","info":"dummy","licenses":"dummy"}
        json.dump(result,out_f)
        json.dump(result_coco,out_f_c)

        # prepare od prediction
    with open(in_od,'r') as in_f, open(out_od,'w') as out_f:
        csv_reader = csv.reader(in_f,delimiter='\t')
        for line in csv_reader:
                id = line[0]
                if id in id_set:
                        out_f.write("\t".join(line)+"\n")

over_lapping_ids_file = "fea_cap_overlapping_ids.list"
id_set = []
if os.path.isfile(over_lapping_ids_file):
    with open(over_lapping_ids_file,'r') as f:
        id_set = set([i.strip() for i in f.readlines()])

total_id = len(id_set)
ratio = 0.1

test_ids = list(id_set)[:int(ratio*total_id)]
print(test_ids[:10])

prepare_fea_cap_od_files(id_set=test_ids)
