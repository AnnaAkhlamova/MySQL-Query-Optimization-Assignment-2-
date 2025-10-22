# MySQL-Query-Optimization-Assignment-2-

## Overview
This project demonstrates SQL query optimization on a sample database with three tables: `customers`, `products`, and `orders`. It shows how to improve query performance using indexes and CTEs.

## Setup
```sql
CREATE DATABASE hw2;
USE hw2;

-- View table data
SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM orders;

-- Check indexes
SHOW INDEXES FROM customers;
SHOW INDEXES FROM products;
SHOW INDEXES FROM orders;

## Unoptimized Query

The following query retrieves customers from the United States (or similar), their total orders, total quantity, total spent, and last order date. It demonstrates common inefficiencies such as DISTINCT usage, non-indexed joins, and filtering on expressions.

## Optimized Query

The optimized query uses:

A CTE (recent_orders) to pre-filter relevant orders

Proper index usage (USE INDEX) to guide the optimizer

Optimized country filtering with LIKE

## Summary

CTE Pre-filtering reduces the number of rows joined.

Proper indexing dramatically improves query performance.

Avoiding DISTINCT and filtering on expressions reduces computation overhead.
