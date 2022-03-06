$env:VENDOR_DIR = 'src/pipdot/_vendor'
$env:CIBUILDWHEEL = '0'
pip install --upgrade --no-compile -t $env:VENDOR_DIR -r requires/vendor.txt
pip freeze  --path $env:VENDOR_DIR | tee $env:VENDOR_DIR\freeze.txt
rm -Force -Recurse $env:VENDOR_DIR\*.dist-info 
rm -Force -Recurse $env:VENDOR_DIR\markupsafe\_speedups.* 
