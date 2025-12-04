-- CreateTable
CREATE TABLE "deleted_bid" (
    "id" SERIAL NOT NULL,
    "title" TEXT NOT NULL,
    "status" TEXT,
    "url" TEXT,
    "location" TEXT,
    "city" TEXT,
    "bid_type" TEXT,

    CONSTRAINT "deleted_bid_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "deleted_bid_title_key" ON "deleted_bid"("title");
