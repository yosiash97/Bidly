import { Test, TestingModule } from '@nestjs/testing';
import { DeletedBidService } from './deleted_bid.service';

describe('DeletedBidService', () => {
  let service: DeletedBidService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [DeletedBidService],
    }).compile();

    service = module.get<DeletedBidService>(DeletedBidService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
