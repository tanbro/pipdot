$env:VENDOR_DIR = 'src/pipdot/_vendor'
$env:CIBUILDWHEEL = '0'
pip install -U --upgrade-strategy=eager --no-compile -t $env:VENDOR_DIR -r requires/vendor.txt
pip freeze  --path $env:VENDOR_DIR | tee $env:VENDOR_DIR/freeze.txt
Remove-Item -Force -Recurse $env:VENDOR_DIR/*.dist-info
Remove-Item -Force -Recurse $env:VENDOR_DIR/markupsafe/_speedups.*
