-- CreateTable
CREATE TABLE "bid" (
    "id" SERIAL NOT NULL,
    "title" TEXT NOT NULL,
    "status" TEXT,
    "url" TEXT,

    CONSTRAINT "bid_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "bid_title_key" ON "bid"("title");
