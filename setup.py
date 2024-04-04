from setuptools import Command


class QTIBinding(Command):
    description = "Generate the QTI bindings"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from subprocess import check_call

        check_call(
            [
                "pyxbgen",
                "-u",
                "http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd",
                "-m",
                "nice_canvas.qti.binding",
            ],
            cwd="src",
        )


if __name__ == "__main__":
    import setuptools
    import setuptools.command.build

    setuptools.command.build.build.sub_commands.insert(0, ("qti_binding", None))
    setuptools.setup(cmdclass={"qti_binding": QTIBinding})
