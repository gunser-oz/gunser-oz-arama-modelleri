#!/bin/sh
# GitHub'ın 100 MB sınırı yüzünden parçalanan tarayıcı modelini birleştirir.
cd "$(dirname "$0")/model/onnx" && cat model_quantized.onnx.part_* > model_quantized.onnx && echo "model_quantized.onnx hazır"
