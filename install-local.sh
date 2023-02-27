set -eux

rm -rf backend/vecsim_app/templates/build  # delete previously built frontend

cd ./frontend
yarn install --no-optional
yarn build

python -m pip install --upgrade pip setuptools wheel

cd ../backend
pip install -e .
cp -r ../frontend/build vecsim_app/templates/

cd ./vecsim_app
chmod +x entrypoint.sh
