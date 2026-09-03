-- ============================================================
-- AI Business Analyst Assistant
-- Database Schema
-- Database: business_analytics
-- ============================================================

CREATE DATABASE IF NOT EXISTS business_analytics;

USE business_analytics;


-- ============================================================
-- 1. CUSTOMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(150),
    city VARCHAR(100),
    region VARCHAR(50),
    customer_segment VARCHAR(50),
    registration_date DATE
);


-- ============================================================
-- 2. PRODUCTS
-- ============================================================

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    unit_cost DECIMAL(12,2),
    selling_price DECIMAL(12,2)
);


-- ============================================================
-- 3. SALES
-- ============================================================

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(12,2),
    total_amount DECIMAL(12,2),
    payment_method VARCHAR(50),
    region VARCHAR(50),
    sale_date DATE,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);


-- ============================================================
-- 4. SALES TARGETS
-- ============================================================

CREATE TABLE IF NOT EXISTS sales_targets (
    target_id INT PRIMARY KEY,
    target_date DATE,
    region VARCHAR(50),
    target_amount DECIMAL(12,2)
);


-- ============================================================
-- 5. CLEANED SALES DATA
-- ============================================================

CREATE TABLE IF NOT EXISTS sales_cleaned (
    customer_id INT,
    payment_method VARCHAR(50),
    product_id INT,
    quantity INT,
    region VARCHAR(50),
    sale_date DATE,
    sale_id INT PRIMARY KEY,
    total_amount DECIMAL(12,2),
    unit_price DECIMAL(12,2)
);


-- ============================================================
-- DATABASE RELATIONSHIPS
-- ============================================================

-- sales_cleaned.product_id → products.product_id
-- sales_cleaned.customer_id → customers.customer_id


-- ============================================================
-- END OF SCHEMA
-- ============================================================