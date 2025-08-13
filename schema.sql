-- schema.sql (run via: psql -U <user> -d <db> -f schema.sql)
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(64) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    available_stocks INT NOT NULL,
    price_per_unit FLOAT NOT NULL,
    tax_percentage FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS purchases (
    id SERIAL PRIMARY KEY,
    customer_email VARCHAR(255) NOT NULL,
    total_amount FLOAT NOT NULL,
    paid_amount FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS purchase_items (
    id SERIAL PRIMARY KEY,
    purchase_id INT REFERENCES purchases(id) ON DELETE CASCADE,
    product_id VARCHAR(64) REFERENCES products(product_id) ON DELETE RESTRICT,
    quantity INT NOT NULL,
    unit_price FLOAT NOT NULL,
    tax_percentage FLOAT NOT NULL
);

-- seed data
INSERT INTO products (product_id, name, available_stocks, price_per_unit, tax_percentage)
VALUES
('P001', 'Apple', 50, 10.0, 5.0),
('P002', 'Banana', 100, 5.0, 2.0),
('P003', 'Milk', 30, 30.0, 12.0),
('P004', 'Orange', 80, 8.0, 5.0),
('P005', 'Mango', 40, 15.0, 5.0),
('P006', 'Pineapple', 25, 25.0, 5.0),
('P007', 'Grapes', 60, 12.0, 5.0),
('P008', 'Watermelon', 15, 50.0, 2.0),
('P009', 'Tomato', 90, 6.0, 2.0),
('P010', 'Potato', 120, 4.0, 2.0),
('P011', 'Onion', 110, 5.0, 2.0),
('P012', 'Cucumber', 70, 7.0, 2.0),
('P013', 'Carrot', 85, 9.0, 2.0),
('P014', 'Broccoli', 40, 20.0, 5.0),
('P015', 'Spinach', 50, 8.0, 2.0),
('P016', 'Eggs (Dozen)', 35, 60.0, 0.0),
('P017', 'Chicken Breast (1kg)', 20, 200.0, 5.0),
('P018', 'Fish (1kg)', 15, 250.0, 5.0),
('P019', 'Cheese (500g)', 25, 180.0, 12.0),
('P020', 'Bread Loaf', 60, 25.0, 5.0)
ON CONFLICT (product_id) DO NOTHING;

