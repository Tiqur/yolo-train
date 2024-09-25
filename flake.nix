{
  description = "A Nix-flake-based Python development environment with build inputs.";

  inputs.nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*.tar.gz";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          # Python and build inputs
          packages = with pkgs; [
            python3                   # Python 3 interpreter
            python3Packages.pip       # Pip package manager for Python
            stdenv.cc.cc.lib          # C compiler and related libraries
            libGL
            glib
          ];

          # Setup Python virtual environment
          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
              pkgs.stdenv.cc.cc
              pkgs.libGL
              pkgs.glib
            ]}
            # Create a virtual environment if not already created
            if [ ! -d ".venv" ]; then
              python3 -m venv .venv
            fi

            # Activate the virtual environment
            source .venv/bin/activate

            # Install non-Nix packages using pip
            pip install --upgrade pip
            pip install ultralytics
            #pip uninstall opencv-python
            #pip install opencv-python-headless
            pip install label-studio

            echo "Python environment with C libraries and pip packages loaded!"
          '';
        };
      });
    };
}

