package com.cse327project.pitlessbucket.feature_pitlessbucket.data.data_source.api

import com.cse327project.pitlessbucket.feature_pitlessbucket.domain.model.FileInfo
import retrofit2.Retrofit

class ApiServiceImpl(private val retrofit: Retrofit) : ApiService {
    private val api = retrofit.create(FileApi::class.java)

    override suspend fun getFiles(): List<FileInfo> {
        return api.getFiles()
    }
}