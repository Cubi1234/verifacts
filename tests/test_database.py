import unittest
from modelo import app, get_db_connection

class TestDatabaseRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_classify_and_db_entry(self):
        # Prueba para el endpoint /classify
        response = self.app.post('/classify', json={"headline": "test headline"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", data)
        self.assertIn("certainty", data)
        
        # Verificar si la entrada fue agregada a la base de datos
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM predicciones WHERE titular=%s ORDER BY fecha_hora DESC LIMIT 1", ("test headline",))
                result = cur.fetchone()
                self.assertIsNotNone(result)
                self.assertEqual(result[1], "test headline")  # Verificar si el titular es correcto

    def test_get_all_entries(self):
        # Prueba para el endpoint /all_entries
        response = self.app.get('/all_entries')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
