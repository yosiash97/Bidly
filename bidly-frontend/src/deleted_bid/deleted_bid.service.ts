import { Injectable } from '@nestjs/common';
import { CreateDeletedBidDto } from './dto/create-deleted_bid.dto';
import { UpdateDeletedBidDto } from './dto/update-deleted_bid.dto';

@Injectable()
export class DeletedBidService {
  create(createDeletedBidDto: CreateDeletedBidDto) {
    return 'This action adds a new deletedBid';
  }

  findAll() {
    return `This action returns all deletedBid`;
  }

  findOne(id: number) {
    return `This action returns a #${id} deletedBid`;
  }

  update(id: number, updateDeletedBidDto: UpdateDeletedBidDto) {
    return `This action updates a #${id} deletedBid`;
  }

  remove(id: number) {
    return `This action removes a #${id} deletedBid`;
  }
}
