# #!/bin/bash


# mkdir dataset

# num_threads=20
# mkdir -p dataset/val
# cd  dataset/val || exit
# mkdir -p images labels

# process_task() {
#     i=$1
#     mkdir -p "$i"
#     cd "$i" || exit


#     python3 ../../../gen.py "$i" > "$i.tex"

#     pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -recorder "./$i.tex"

#     pdftoppm -png "./$i.pdf" "$i"

#     cd ..

#     mv "$i/$i-1.png" "images/$i.png"
#     mv "$i/$i.txt" "labels/$i.txt"

#     rm -rf "$i"
# }

# for i in $(seq 1 100); do
#     process_task "$i" &
    
#     while [ "$(jobs | wc -l)" -ge "$num_threads" ]; do
#         sleep 1 
#     done
# done

# num_threads=20
# mkdir -p dataset/train
# cd  dataset/train || exit
# mkdir -p images labels

# process_task() {
#     i=$1
#     mkdir -p "$i"
#     cd "$i" || exit


#     python3 ../../../gen.py "$i" > "$i.tex"

#     pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -recorder "./$i.tex"

#     pdftoppm -png "./$i.pdf" "$i"

#     cd ..

#     mv "$i/$i-1.png" "images/$i.png"
#     mv "$i/$i.txt" "labels/$i.txt"

#     rm -rf "$i"
# }

# for i in $(seq 1 100); do
#     process_task "$i" &
    
#     while [ "$(jobs | wc -l)" -ge "$num_threads" ]; do
#         sleep 1 
#     done
# done

# wait
#!/bin/bash

set -e

mkdir -p dataset/val/images dataset/val/labels
mkdir -p dataset/train/images dataset/train/labels

### ---------------- VAL ---------------- ###
val_task() {
    i=$1
    mkdir -p "dataset/val/tmp_$i"
    cd "dataset/val/tmp_$i" || exit

    python3 ../../../gen.py "$i" > "$i.tex"
    pdflatex -interaction=nonstopmode "$i.tex"
    pdftoppm -png "$i.pdf" "$i"

    cd ..

    mv "tmp_$i/$i-1.png" "images/$i.png"
    mv "tmp_$i/$i.txt"  "labels/$i.txt"

    rm -rf "tmp_$i"
}

num_threads=3
for i in $(seq 1 100); do
    val_task "$i" &
    while [ "$(jobs -r | wc -l)" -ge "$num_threads" ]; do sleep 1; done
done
wait

### ---------------- TRAIN ---------------- ###
train_task() {
    i=$1
    mkdir -p "dataset/train/tmp_$i"
    cd "dataset/train/tmp_$i" || exit

    python3 ../../../gen.py "$i" > "$i.tex"
    pdflatex -interaction=nonstopmode "$i.tex"
    pdftoppm -png "$i.pdf" "$i"

    cd ..

    mv "tmp_$i/$i-1.png" "images/$i.png"
    mv "tmp_$i/$i.txt"  "labels/$i.txt"

    rm -rf "tmp_$i"
}

num_threads=3
for i in $(seq 1 100); do
    train_task "$i" &
    while [ "$(jobs -r | wc -l)" -ge "$num_threads" ]; do sleep 1; done
done
wait

