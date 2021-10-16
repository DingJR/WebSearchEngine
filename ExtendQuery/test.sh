python ExtendWordQue.py
cp WordExtendOutput trec_eval.9.0/
cd trec_eval.9.0/
./trec_eval StdAns  WordExtendOutput >RESULT
cat RESULT
mv RESULT ../WordExtendResult
cd ..
