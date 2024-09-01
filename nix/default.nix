let
    pkgs = (import (builtins.fetchTarball {
        url = "https://github.com/NixOS/nixpkgs/archive/63dacb46bf939521bdc93981b4cbb7ecb58427a0.zip";
        sha256 = "1lr1h35prqkd1mkmzriwlpvxcb34kmhc9dnr48gkm8hh089hifmx";
    }) { });
    stdenv = pkgs.stdenv;
in pkgs.mkShell rec {
    name = "scraper";
    shellHook = ''
        source nix/.bashrc
    '';
    buildInputs = (with pkgs; [
        bashInteractive
        (pkgs.python3.buildEnv.override {
            ignoreCollisions = true;
            extraLibs = with pkgs.python3.pkgs; [
                ipython
                nose
                requests
                beautifulsoup4
                celery[redis]
                redis
            ];
        })
        pkgs.redis
    ]);
}
