from transformers import AutoModelForSeq2SeqLM
from allennlp.models.model import Model
from allennlp.nn import InitializerApplicator
import json
from utils import supportsetpred
from transformers import AutoTokenizer
import os

import torch

class T5model(Model):
    def __init__(self, pretrainedfile,
                 initializer: InitializerApplicator = InitializerApplicator()):
        super(T5model, self).__init__(None, None)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(pretrainedfile)
        self.config = self.model.config
        InitializerApplicator(self)
    
    def init(self):
        self.model = AutoModelForSeq2SeqLM.from_config(self.config)

    def forward(self,inputid,mask=None,outputid=None,outmask=None,label=None,**kargs):

        inputid = inputid.long()
                
        if label is not None:
            outputid = outputid.long()

            
            decoder_embed_device = self.model.decoder.embed_tokens.weight.device
            decoder_embeds_init = self.model.decoder.embed_tokens.forward(outputid.to(decoder_embed_device))

            ### add noise to embeds
            decoder_input_mask = outmask.to(decoder_embeds_init) # B x L  
            decoder_input_lengths = torch.sum(decoder_input_mask, 1) 
            
            decoder_noise_ = torch.zeros_like(decoder_embeds_init).uniform_(-1,1)  
            decoder_delta = decoder_noise_ * decoder_input_mask.unsqueeze(2)   
            decoder_dims = decoder_input_lengths * decoder_embeds_init.size(-1)  
            decoder_mag = 5 / torch.sqrt(decoder_dims)  
            decoder_delta = (decoder_delta * decoder_mag.view(-1, 1, 1)).detach()   
            

            label = label.masked_fill(label==-1,-100)
            output_dict = self.model(input_ids = inputid,attention_mask=mask, decoder_attention_mask=outmask, decoder_inputs_embeds=decoder_delta + decoder_embeds_init, labels=label, return_dict=True)  
        else:
            return {'output':self.model.generate(inputid,max_length=200)}
        return output_dict

class spanT5model(Model):
    def __init__(self, pretrainedfile,
                 initializer: InitializerApplicator = InitializerApplicator()):
        super(spanT5model, self).__init__(None, None)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(pretrainedfile)
        self.config = self.model.config
        InitializerApplicator(self)
    
    def init(self):
        self.model = AutoModelForSeq2SeqLM.from_config(self.config)

    def forward(self,inputid,mask=None,outputid=None,outmask=None,label=None,**kargs):
        inputid = inputid.long()
        if label is not None:
            outputid = outputid.long()
            label = label.masked_fill(label==-1,-100)
            output_dict = self.model(input_ids = inputid,attention_mask=mask, decoder_input_ids=outputid, decoder_attention_mask=outmask, labels=label, return_dict=True)
        else:
            return {'output':self.model.generate(inputid,max_length=200)}
        return output_dict