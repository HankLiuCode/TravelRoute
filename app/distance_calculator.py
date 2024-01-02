class DistanceCalculator:
    def __init__(self, attractions, matrix):
        ROWS, COLS = len(matrix), len(matrix[0])
        if ROWS != COLS: raise Exception("Invalid matrix")
        if ROWS != len(attractions): raise Exception("Attraction and Matrix doesn't match")

        self.attractions = attractions
        self.matrix = matrix

    def calculate(self, from_attraction, to_attraction):
        from_index = self.attractions.index(from_attraction)
        to_index = self.attractions.index(to_attraction)
        return self.matrix[from_index][to_index]