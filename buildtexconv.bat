rmdir /Q /S DirectXTex
git clone https://github.com/microsoft/DirectXTex.git
cd DirectXTex\Texconv
for /f "usebackq delims=" %%i in (`vswhere.exe -prerelease -latest -property installationPath`) do (
  if exist "%%i\VC\Auxiliary\build\vcvarsall.bat" (
    call "%%i\VC\Auxiliary\build\vcvarsall.bat" x64
  )
)
msbuild Texconv_Desktop_2019.vcxproj /p:Configuration=Release /p:Platform=x64
copy Bin\Desktop_2019\x64\Release\texconv.exe ..\..
cd ..\..
rmdir /Q /S DirectXTex
exit