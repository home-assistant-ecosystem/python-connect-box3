{
  description = "python-connect-box3 dev shell with pytest and ruff";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python313;
        pythonEnv = python.withPackages (ps: with ps; [
          # runtime
          cyclopts
          httpx
          mashumaro
          rich
          # test
          pytest
          pytest-asyncio
          pytest-httpx
          syrupy
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [ pythonEnv pkgs.ruff ];

          shellHook = ''
            export PYTHONPATH="$PWD:$PYTHONPATH"
          '';
        };

        checks = {
          pytest = pkgs.runCommand "pytest" {
            buildInputs = [ pythonEnv pkgs.cacert ];
            SSL_CERT_FILE = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";
          } ''
            cp -r ${self} $TMPDIR/src
            chmod -R u+w $TMPDIR/src
            export PYTHONPATH="$TMPDIR/src:$PYTHONPATH"
            export HOME="$TMPDIR"
            cd $TMPDIR/src
            pytest --tb=short
            touch $out
          '';

          ruff-check = pkgs.runCommand "ruff-check" { buildInputs = [ pkgs.ruff ]; } ''
            export RUFF_CACHE_DIR="$TMPDIR/.ruff_cache"
            cd ${self}
            ruff check .
            touch $out
          '';

          ruff-format = pkgs.runCommand "ruff-format" { buildInputs = [ pkgs.ruff ]; } ''
            export RUFF_CACHE_DIR="$TMPDIR/.ruff_cache"
            cd ${self}
            ruff format --check .
            touch $out
          '';
        };
      });
}
