docker run --network=host \
    -e NERO_TARGET=http://localhost:8000/ \
    -e NERO_DICT_PATH=/user_dict.txt \
    -v ~/dict.txt:/user_dict.txt \
    nero
