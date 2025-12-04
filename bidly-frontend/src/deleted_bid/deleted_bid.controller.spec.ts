import { Test, TestingModule } from '@nestjs/testing';
import { DeletedBidController } from './deleted_bid.controller';
import { DeletedBidService } from './deleted_bid.service';

describe('DeletedBidController', () => {
  let controller: DeletedBidController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [DeletedBidController],
      providers: [DeletedBidService],
    }).compile();

    controller = module.get<DeletedBidController>(DeletedBidController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
