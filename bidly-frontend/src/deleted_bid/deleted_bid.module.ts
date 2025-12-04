import { Module } from '@nestjs/common';
import { DeletedBidService } from './deleted_bid.service';
import { DeletedBidController } from './deleted_bid.controller';

@Module({
  controllers: [DeletedBidController],
  providers: [DeletedBidService],
})
export class DeletedBidModule {}
