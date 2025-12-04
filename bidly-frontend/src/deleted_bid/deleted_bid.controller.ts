import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { DeletedBidService } from './deleted_bid.service';
import { CreateDeletedBidDto } from './dto/create-deleted_bid.dto';
import { UpdateDeletedBidDto } from './dto/update-deleted_bid.dto';

@Controller('deleted-bid')
export class DeletedBidController {
  constructor(private readonly deletedBidService: DeletedBidService) {}

  @Post()
  create(@Body() createDeletedBidDto: CreateDeletedBidDto) {
    return this.deletedBidService.create(createDeletedBidDto);
  }

  @Get()
  findAll() {
    return this.deletedBidService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.deletedBidService.findOne(+id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateDeletedBidDto: UpdateDeletedBidDto) {
    return this.deletedBidService.update(+id, updateDeletedBidDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.deletedBidService.remove(+id);
  }
}
