cd ./frontend

yarn install --no-optional
yarn build

cd ..

python -m pip install --upgrade pip setuptools wheel

cd ./backend

pip install -e .

rm -rf vecsim_app/templates/build
cp -r ../frontend/build vecsim_app/templates/

cd ./vecsim_app
chmod +x entrypoint.sh
