#!/bin/sh
# GitHub'ın 100 MB dosya sınırı yüzünden parçalanan ağırlıkları birleştirir.
cd "$(dirname "$0")" && cat model.safetensors.part_* > model.safetensors && echo "model.safetensors hazır"
