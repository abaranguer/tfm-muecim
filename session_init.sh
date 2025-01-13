echo "Set git global properties"
git config --global user.email "abaranguer@gmail.com"
git config --global user.name "Albert Baranguer i Codina"
echo
echo "copy code, dataset, labels to /content"
cp /content/drive/MyDrive/TFM-MUECIM/*.py /content
cp /content/drive/MyDrive/TFM-MUECIM/*.txt /content
cp /content/drive/MyDrive/TFM-MUECIM/*.csv /content
cp /content/drive/MyDrive/TFM-MUECIM/data/datasets/EURLEX57K/*.json /content
echo
echo "Install emacs"
apt install emacs
echo
echo "Install joe"
apt install joe
echo
echo "Done!"

