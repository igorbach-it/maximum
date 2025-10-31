from __future__ import annotations
from typing import List, Tuple

Number = float | int

class Matrix:
    def __init__(self, rows: List[List[Number]]):
        if not rows or not rows[0]:
            raise ValueError("Matrix cannot be empty")
        n = len(rows[0])
        for r in rows:
            if len(r) != n:
                raise ValueError("All rows must have same length")
        self._m = [[float(x) for x in r] for r in rows]
        self._r, self._c = len(rows), n

    @property
    def shape(self) -> Tuple[int, int]:
        return self._r, self._c

    def __repr__(self) -> str:
        return "Matrix([" + ", ".join(str(r) for r in self._m) + "])"

    @staticmethod
    def zeros(r: int, c: int) -> "Matrix":
        return Matrix([[0.0]*c for _ in range(r)])

    @staticmethod
    def identity(n: int) -> "Matrix":
        m = Matrix.zeros(n, n)
        for i in range(n):
            m._m[i][i] = 1.0
        return m

    def __add__(self, o: "Matrix") -> "Matrix":
        if self.shape != o.shape:
            raise ValueError("Shapes must match for addition")
        r, c = self.shape
        out = Matrix.zeros(r, c)
        for i in range(r):
            for j in range(c):
                out._m[i][j] = self._m[i][j] + o._m[i][j]
        return out

    def __sub__(self, o: "Matrix") -> "Matrix":
        if self.shape != o.shape:
            raise ValueError("Shapes must match for subtraction")
        r, c = self.shape
        out = Matrix.zeros(r, c)
        for i in range(r):
            for j in range(c):
                out._m[i][j] = self._m[i][j] - o._m[i][j]
        return out

    def __mul__(self, o) -> "Matrix":
        if isinstance(o, (int, float)):
            r, c = self.shape
            out = Matrix.zeros(r, c)
            for i in range(r):
                for j in range(c):
                    out._m[i][j] = self._m[i][j] * float(o)
            return out
        if isinstance(o, Matrix):
            r1, c1 = self.shape
            r2, c2 = o.shape
            if c1 != r2:
                raise ValueError("Inner dimensions must match")
            out = Matrix.zeros(r1, c2)
            for i in range(r1):
                for k in range(c1):
                    aik = self._m[i][k]
                    if aik == 0.0:
                        continue
                    for j in range(c2):
                        out._m[i][j] += aik * o._m[k][j]
            return out
        return NotImplemented

    def __rmul__(self, o) -> "Matrix":
        if isinstance(o, (int, float)):
            return self * o
        return NotImplemented

    def __truediv__(self, o: "Matrix") -> "Matrix":
        return self * o.inverse()

    def determinant(self) -> float:
        r, c = self.shape
        if r != c:
            raise ValueError("Square only")
        A = [row[:] for row in self._m]
        n = r
        det = 1.0
        for i in range(n):
            p = max(range(i, n), key=lambda rr: abs(A[rr][i]))
            if abs(A[p][i]) == 0.0:
                return 0.0
            if p != i:
                A[i], A[p] = A[p], A[i]
                det *= -1.0
            det *= A[i][i]
            piv = A[i][i]
            for r2 in range(i+1, n):
                f = A[r2][i] / piv
                if f != 0.0:
                    for j in range(i, n):
                        A[r2][j] -= f * A[i][j]
        return det

    def inverse(self) -> "Matrix":
        r, c = self.shape
        if r != c:
            raise ValueError("Square only")
        n = r
        A = [row[:] for row in self._m]
        I = Matrix.identity(n)._m
        for i in range(n):
            p = max(range(i, n), key=lambda rr: abs(A[rr][i]))
            if abs(A[p][i]) == 0.0:
                raise ValueError("Singular")
            if p != i:
                A[i], A[p] = A[p], A[i]
                I[i], I[p] = I[p], I[i]
            piv = A[i][i]
            for j in range(n):
                A[i][j] /= piv
                I[i][j] /= piv
            for r2 in range(n):
                if r2 == i:
                    continue
                f = A[r2][i]
                if f != 0.0:
                    for j in range(n):
                        A[r2][j] -= f * A[i][j]
                        I[r2][j] -= f * I[i][j]
        return Matrix(I)
