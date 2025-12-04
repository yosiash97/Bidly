/*
  Warnings:

  - You are about to drop the `deleted_bid` table. If the table is not empty, all the data it contains will be lost.

*/
-- AlterTable
ALTER TABLE "bid" ADD COLUMN     "deletedAt" TIMESTAMP(3);

-- DropTable
DROP TABLE "deleted_bid";
