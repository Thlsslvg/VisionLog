class Rejection:

    def __init__(self, camera, status, defect, time, filename):
        self.camera = camera
        self.status = status
        self.defect = defect
        self.time = time
        self.filename = filename

    def show(self):
        print(f"Camera  : {self.camera}")
        print(f"Status  : {self.status}")
        print(f"Defect  : {self.defect}")
        print(f"Time    : {self.time}")
        print(f"File    : {self.filename}")