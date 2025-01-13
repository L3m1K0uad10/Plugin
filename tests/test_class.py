import pytest
import source.class_ as class_



class TestClass:

    def setup_method(self, method): # pytest setup fixture
        self.Rectangle1 = class_.Rectangle(4, 2)

    def teardown_method(self, method):
        print("T E S T - C O M P L E T E D")

    def test_circle(self):
        Circle1 = class_.Circle(2)
        result = Circle1.area()
        assert result == 12.566370614359172

    def test_rectangle(self):
        result1 = self.Rectangle1.perimeter()
        result2 = self.Rectangle1.area()
        assert result1 == 12 and result2 == 8