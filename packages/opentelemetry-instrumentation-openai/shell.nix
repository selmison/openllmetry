{ pkgs ? import <nixpkgs> { } }:
let
  unstable = import <unstable> { };
in
with unstable;
pkgs.mkShell {
  nativeBuildInputs = [
    python39
    # poetry
    python39Packages.pip
  ];
}
