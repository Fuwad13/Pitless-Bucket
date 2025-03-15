package com.cse327project.pitlessbucket.feature_pitlessbucket.data.data_source.api

import com.cse327project.pitlessbucket.feature_pitlessbucket.domain.model.FileInfo
import retrofit2.http.GET

interface FileApi {
    @GET("files")
    suspend fun getFiles(): List<FileInfo>
}