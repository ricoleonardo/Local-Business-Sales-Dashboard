CREATE TABLE `customers` (
  `id` integer PRIMARY KEY,
  `name` varchar(255),
  `email` varchar(255)
);

CREATE TABLE `orders` (
  `id` integer PRIMARY KEY,
  `product` varchar(255),
  `amount` DECIMAL(7,2),
  `order_date` DATE,
  `customers_id` integer,
  `transaction_id` integer
);

CREATE TABLE `transactions` (
  `id` integer PRIMARY KEY,
  `transaction_date` DATE
);

ALTER TABLE `orders` ADD FOREIGN KEY (`customers_id`) REFERENCES `customers` (`id`);

ALTER TABLE `orders` ADD FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`);
