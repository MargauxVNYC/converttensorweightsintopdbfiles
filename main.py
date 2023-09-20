import csv
import numpy as np
import pandas as pd
import os
os.getcwd() # provides the full file path for the current working directory
os.listdir() # provides a list of all files in the current working directory

global final_name

#This function matches the name of the weight files with the name of the pdb protein files.

def get_file_names_with_strings(str_list):

    full_list = os.listdir("/Users/userfolder/ConvertTensorWeights/done_matched_pdb")
    for word in full_list:
        print("this is word", word)
        if not word.startswith('.') and str_list in word:
            final_name = word
            print("this is final_name", final_name)

            return final_name

#this function fixes some texts in the files.
def text_num_split(item):
    for index, letter in enumerate(item, 0):
        if letter.isdigit():
            return [item[:index],item[index:]]

directory = '/Users/userfolder/ConvertTensorWeights/last_numpy_attn_weights'

#This for loop goes through the weight numpy files, finds the pdb files that matches replaces a the b factor column with the weight values.
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if not filename.startswith('.') and os.path.isfile(f):
        print("this is a file", filename)
        pdb_name = os.path.basename(f).split("_")[2]
        print("pdb name", pdb_name)
        # checking if it is a file

        pdb_file = get_file_names_with_strings(pdb_name)
        #pdb_file = "AF-Q6P2D8-F1-model_v4.pdb"
        print("pdb_file", pdb_file)

        protein_file = os.path.join(f'/Users/userfolder/ConvertTensorWeights/done_matched_pdb/{pdb_file}')
        print("this is protein_file", protein_file)

        outfile = open(protein_file, "r")
        data = outfile.readlines()
        new_data = []

        n = 0
        for line in data:
            if "ATOM" in line:
               n = n + 1
               line_new = line.split()
               #print("new atom protein line number", line_new[5])
               #print("new atom protein line", line)
               new_data.append(line)

        #print("this is new_data", new_data)



        c = np.load(f"/Users/userfolder/ConvertTensorWeights/done_numpy_attn_weights/{filename}")
        print("this is numpy shape", c.shape)
        np.set_printoptions(threshold=np.inf)
        no_rows = c.shape[0]
        print("number of rows", no_rows)

        no = 1
        #this for loop uses the 16 columns of weight values
        for j in range(16):
            no = no + 1
            k = c[ :, no]
            print(f"for j this is no {no}")
            n5 = 1
            h = open(f"/Users/userfolder/ConvertTensorWeights/new_weights_folder3/fixed_{filename}_{no}.pdb" , "w+")

            for v in k:

                print("this is v", v)
                    #this for loop for then goes through each dimension row of the weights and goes through the protein data and
                    #finds the atom number that matches and substitutes the weights in the b-factor column

                for line in new_data:
                    print("this is line", line)
                    line_new = line.split()
                    print("length of line", len(line_new))
                    print("line_new", line_new)
                    if len(line_new) != 12:
                        if len(line_new[4]) != 1:
                            print("spot 5", line_new[4])
                            insert_split = text_num_split(line_new[4])
                            print("insert_split", insert_split)
                            line_new.insert(4, insert_split[0])
                            line_new[5] = insert_split[1]
                            print("line new after another split", line_new)
                        spot_list = 0
                        for string in line_new:
                            t = string.split('.')
                            print("this is t", t)
                            if len(t)>2:
                                print('this is string', len(t), string)
                                splt_char = "-"
                                # initializing K
                                K = 2

                                # Printing original string
                                print("The original string is : " + str(string))

                                # Split string on Kth Occurrence of Character
                                # using split() + join()
                                temp = string.split(splt_char)
                                res = splt_char.join(temp[:K]), splt_char.join(temp[K:])

                                print('this is res', res)
                                print("this is old line_new", line_new)
                                string = res
                                line_new.insert(spot_list, res[0])
                                second_spot = spot_list + 1
                                line_new[second_spot] = res[1]
                                print("new line_new", line_new)

                            spot_list = spot_list + 1

                    print("this is line_new", line_new)
                    six_value = int(line_new[5])
                    print("this is six_value and v", six_value, n5)
                    if six_value == n5 and n5 < no_rows:
                        print("match of six value")
                        #row5 = round(row5, 4)
                        print("row5 round", v)
                        new_num = str(v)
                        print("new_num", new_num)

                        new_num = new_num.rjust(len(new_num)+1)
                        print("new num with space", new_num)
                        line_fixed = new_num.join([line[:60],line[66:]])
                        print("this is line fixed with space", line_fixed)
                        h.write(line_fixed)


                n5 = n5 + 1
            h.close()




