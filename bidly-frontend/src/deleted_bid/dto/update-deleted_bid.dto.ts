import { PartialType } from '@nestjs/mapped-types';
import { CreateDeletedBidDto } from './create-deleted_bid.dto';

export class UpdateDeletedBidDto extends PartialType(CreateDeletedBidDto) {}
